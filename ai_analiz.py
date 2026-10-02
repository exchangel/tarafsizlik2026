# ai_analiz.py
import pandas as pd
from google import genai
import json
import re
import time
import os

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("Error: GEMINI_API_KEY environment variable not found.")
    exit(1)
client = genai.Client(api_key=API_KEY)

# Desteklenen ve sirayla denenecek kararli modeller
DENENECEK_MODELLER = [
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
    "gemini-3.8-flash"
]

# ------------------------------------------------------------------------------
# 2. YAPILANDIRMA VE VERI YUKLEME
# ------------------------------------------------------------------------------
# config.json dosyasindan izin verilen standart etiketleri okuma
try:
    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)
    izin_verilen_etiketler = config.get("etiketler", [])
except FileNotFoundError:
    print("HATA: config.json dosyasi bulunamadi.")
    exit(1)

# Veri setini okuma
try:
    df = pd.read_csv("haber_veriseti.csv")
    if df.empty:
        print("BİLGİ: Yeni islenecek haber bulunamadi (haber_veriseti.csv bos). Islem sonlandiriliyor.")
        # Eger yeni haber yoksa ama master veri setinden 30 gunluk silme islemi yapilmasi gerekiyorsa
        # burada da 30 gun temizligi cagrilabilir, ama sadelik adina cikiyoruz.
        exit(0)
except FileNotFoundError:
    print("HATA: haber_veriseti.csv bulunamadi. Once veri_cekici.py calistirilmalidir.")
    exit(1)

# Token verimliligi ve islem hizi icin modele yalnizca ID ve Baslik gonderiyoruz
haber_listesi = [{"id": index, "baslik": row["Baslik"]} for index, row in df.iterrows()]

# ------------------------------------------------------------------------------
# 3. ANALIZ TALIMATI (PROMPT) HAZIRLAMA
# ------------------------------------------------------------------------------
prompt = f"""
Sen tarafsiz ve profesyonel bir medya analistisin. Asagida Turkiye gundemine ait haber basliklari JSON formatinda verilmistir.

GOREVLERIN:
1. AYNI siyasi, ekonomik, hukuki veya toplumsal olayi/gelismeyi anlatan haberleri tek bir grupta birlestir.
2. Magazin, kedi-kopek, basit trafik kazalari, hava durumu gibi ulusal gundemle ilgisi olmayan 3. sayfa haberlerini SADECE "Ilgisiz" adli tek bir grupta topla. Bunlara etiket atama.
3. Her gecerli grup icin nesnel, tarafsiz ve profesyonel bir 'konu_basligi' belirle (Ornek: 'Merkez Bankasi Politika Faizi Karari', 'Anayasa Mahkemesi Karari').
4. Her grup icin bu olayin tam olarak ne oldugunu anlatan nesnel, tarafsiz ve tek cumlelik kisa bir 'grup_ozeti' yaz.
5. Her grup icin SADECE asagidaki listeden en uygun 1, 2 veya 3 etiketi sec. Bu liste disindan ASLA baska etiket kullanma:
{json.dumps(izin_verilen_etiketler, ensure_ascii=False)}

CIKTI FORMATI:
SADECE asagidaki JSON formatinda cikti ver. Ekstra aciklama metni yazma:
[
  {{
    "konu_basligi": "Konu Adi",
    "grup_ozeti": "Olayin tarafsiz ve 1 cumlelik ozeti.",
    "etiketler": ["#etiket1", "#etiket2"],
    "haber_idleri": [0, 5, 12]
  }}
]

Haber Listesi:
{json.dumps(haber_listesi, ensure_ascii=False)}
"""

print(f"Toplam {len(haber_listesi)} haber basligi analiz icin hazirlaniyor...")

# ------------------------------------------------------------------------------
# 4. MODELIN CAGIRILMASI (HATA VE MODEL YEDEGI ILE)
# ------------------------------------------------------------------------------
yanit_metni = None

for model_adi in DENENECEK_MODELLER:
    try:
        print(f"Analiz '{model_adi}' modeli ile baslatiliyor...")
        chat = client.chats.create(model=model_adi)
        response = chat.send_message(prompt)
        yanit_metni = response.text.strip()
        print(f"'{model_adi}' modelinden yanit basariyla alindi.")
        break
    except Exception as e:
        print(f"UYARI: '{model_adi}' ulasilamadi veya mesgul ({e}). Diger model deneniyor...")
        time.sleep(2)

if not yanit_metni:
    print("HATA: Hicbir modelden yanit alinamadi. Lutfen API anahtarinizi veya internet baglantinizi kontrol edin.")
    exit(1)

# ------------------------------------------------------------------------------
# 5. YANITIN ISLENMESI VE VERI SETINE ISLENMESI
# ------------------------------------------------------------------------------
try:
    # Markdown kod bloklarini (```json ... ```) temizleme
    temiz_json = re.sub(r"^```(?:json)?\s*", "", yanit_metni, flags=re.MULTILINE)
    temiz_json = re.sub(r"```$", "", temiz_json, flags=re.MULTILINE).strip()

    gruplar = json.loads(temiz_json)

    # DataFrame alanlarini hazirlama
    df["Grup_Basligi"] = "Grup Yok"
    df["Etiketler"] = ""
    df["Grup_Ozeti"] = ""

    gecerli_grup_sayisi = 0
    eslesen_haber_sayisi = 0

    # Donen gruplari DataFrame ile eslestirme
    for grup in gruplar:
        konu_basligi = grup.get("konu_basligi", "")
        etiketler = grup.get("etiketler", [])
        haber_idleri = grup.get("haber_idleri", [])
        ozet = grup.get("grup_ozeti", "")

        # "Ilgisiz" veya "İlgisiz" olarak filtrelenen haberleri dahil etmiyoruz
        if konu_basligi not in ["Ilgisiz", "İlgisiz"]:
            gecerli_grup_sayisi += 1
            for haber_id in haber_idleri:
                if haber_id in df.index:
                    df.at[haber_id, "Grup_Basligi"] = konu_basligi
                    df.at[haber_id, "Etiketler"] = ", ".join(etiketler)
                    df.at[haber_id, "Grup_Ozeti"] = ozet
                    eslesen_haber_sayisi += 1

    # Nitelikli haberleri filtreleme
    temiz_df_yeni = df[df["Grup_Basligi"] != "Grup Yok"].copy()

    # ------------------------------------------------------------------------------
    # 6. MASTER VERI SETI ILE BIRLESTIRME VE 30 GUNLUK PENCERE
    # ------------------------------------------------------------------------------
    yeni_dosya_adi = "analizli_haber_veriseti.csv"
    try:
        df_master = pd.read_csv(yeni_dosya_adi)
        # Yeni analiz edilenleri ekle
        df_master = pd.concat([df_master, temiz_df_yeni], ignore_index=True)
    except FileNotFoundError:
        df_master = temiz_df_yeni
    
    # 30 Gunluk pencereyi uygula
    if not df_master.empty and "Tarih" in df_master.columns:
        # Tarih formatlarini duzenle ve 30 gunden eskileri sil
        df_master["Tarih"] = pd.to_datetime(df_master["Tarih"], errors="coerce", utc=True).dt.tz_localize(None)
        otuz_gun_once = pd.Timestamp.now() - pd.Timedelta(days=30)
        df_master = df_master[df_master["Tarih"] >= otuz_gun_once]
        # Tekrar string'e cevirerek CSV formatini koru
        df_master["Tarih"] = df_master["Tarih"].dt.strftime("%Y-%m-%d %H:%M:%S")

    # Sonuclari CSV dosyasina kaydetme
    df_master.to_csv(yeni_dosya_adi, index=False, encoding="utf-8-sig")

    print("-" * 60)
    print("Analiz basariyla tamamlandi.")
    print(f"Olusturulan Gecerli Konu Grubu Sayisi: {gecerli_grup_sayisi}")
    print(f"Gruplanan Nitelikli Haber Sayisi: {eslesen_haber_sayisi}")
    print(f"Master veri setinde toplam tutulan haber sayisi: {len(df_master)}")
    print(f"Sonuclar '{yeni_dosya_adi}' dosyasina kaydedildi.")

except json.JSONDecodeError:
    print("HATA: Yapay zekadan gelen yanit JSON formatina donusturulemedi.")
    print("Gelen Yanit:")
    print(yanit_metni)
except Exception as e:
    print(f"HATA: Beklenmeyen bir sorun olustu: {e}")