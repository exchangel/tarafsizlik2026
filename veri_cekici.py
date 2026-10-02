# veri_cekici.py
import feedparser
import pandas as pd
from datetime import datetime

# Ag istekleri icin standart tarayici kimligi (User-Agent).
# Bazi haber siteleri bot/script engellemesi yaptigi icin bu baslik gereklidir.
TARAYICI_BASLIGI = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Her kaynaktan cekilecek maksimum haber adedi.
# Gelistirme asamasinda kota/hiz icin 10-15 arasi tutulabilir;
# canli sistemde bu sayiyi ihtiyaca gore artirabilirsiniz.
KAYNAK_BASINA_HABER_LIMITI = 15

# RSS baglanti zaman asimi suresi (saniye)
ZAMAN_ASIMI = 10

# ==============================================================================
# KAYNAK LISTESI
# Yeni bir kaynak eklemek icin asagidaki sozluk yapisina ekleme yapabilirsiniz:
# "Kaynak Adi": {"url": "RSS_ADRESI", "gorus": "KATEGORI_ADI"}
# ==============================================================================
rss_kaynaklari = {
    # --------------------------------------------------------------------------
    # 1. MUHAFAZAKAR / IKTIDAR CIZGISI (12 Kaynak)
    # --------------------------------------------------------------------------
    "Sabah": {
        "url": "https://www.sabah.com.tr/rss/gundem.xml",
        "gorus": "Muhafazakar / İktidar Çizgisi"
    },
    "Yeni Şafak": {
        "url": "https://www.yenisafak.com/rss",
        "gorus": "Muhafazakar / İktidar Çizgisi"
    },
    "TRT Haber": {
        "url": "https://www.trthaber.com/gundem_articles.rss",
        "gorus": "Muhafazakar / İktidar Çizgisi"
    },
    "Anadolu Ajansı": {
        "url": "https://www.aa.com.tr/tr/rss/default?cat=guncel",
        "gorus": "Muhafazakar / İktidar Çizgisi"
    },
    "Akşam": {
        "url": "https://www.aksam.com.tr/rss/rss.asp?cat=guncel",
        "gorus": "Muhafazakar / İktidar Çizgisi"
    },
    "Hürriyet": {
        "url": "https://www.hurriyet.com.tr/rss/anasayfa",
        "gorus": "Muhafazakar / İktidar Çizgisi"
    },
    "Milliyet": {
        "url": "https://www.milliyet.com.tr/rss/rssnew/gundemrss.xml",
        "gorus": "Muhafazakar / İktidar Çizgisi"
    },
    "Star": {
        "url": "https://www.star.com.tr/rss/rss.asp",
        "gorus": "Muhafazakar / İktidar Çizgisi"
    },
    "A Haber": {
        "url": "https://www.ahaber.com.tr/rss/gundem.xml",
        "gorus": "Muhafazakar / İktidar Çizgisi"
    },
    "Yeni Akit": {
        "url": "https://www.yeniakit.com.tr/rss/haber/gundem",
        "gorus": "Muhafazakar / İktidar Çizgisi"
    },
    "Diriliş Postası": {
        "url": "https://www.dirilispostasi.com/rss",
        "gorus": "Muhafazakar / İktidar Çizgisi"
    },
    "Ensonhaber": {
        "url": "https://www.ensonhaber.com/rss/ensonhaber.xml",
        "gorus": "Muhafazakar / İktidar Çizgisi"
    },

    # --------------------------------------------------------------------------
    # 2. MERKEZ / BAGIMSIZ (12 Kaynak)
    # --------------------------------------------------------------------------
    "Habertürk": {
        "url": "https://www.haberturk.com/rss/kategori/gundem.xml",
        "gorus": "Merkez / Bağımsız"
    },
    "NTV": {
        "url": "https://www.ntv.com.tr/gundem.rss",
        "gorus": "Merkez / Bağımsız"
    },
    "BBC Türkçe": {
        "url": "https://feeds.bbci.co.uk/turkce/rss.xml",
        "gorus": "Merkez / Bağımsız"
    },
    "DW Türkçe": {
        "url": "https://rss.dw.com/xml/rss-tur-all",
        "gorus": "Merkez / Bağımsız"
    },
    "Euronews Türkçe": {
        "url": "https://tr.euronews.com/rss?level=theme&name=news",
        "gorus": "Merkez / Bağımsız"
    },
    "Independent Türkçe": {
        "url": "https://www.indyturk.com/rss.xml",
        "gorus": "Merkez / Bağımsız"
    },
    "Gazete Pencere": {
        "url": "https://gazetepencere.com/feed/",
        "gorus": "Merkez / Bağımsız"
    },
    "Medyascope": {
        "url": "https://medyascope.tv/feed/",
        "gorus": "Merkez / Bağımsız"
    },
    "Bloomberg HT": {
        "url": "https://www.bloomberght.com/rss",
        "gorus": "Merkez / Bağımsız"
    },
    "Dünya Gazetesi": {
        "url": "https://www.dunya.com/rss",
        "gorus": "Merkez / Bağımsız"
    },
    "Ekonomim": {
        "url": "https://www.ekonomim.com/rss",
        "gorus": "Merkez / Bağımsız"
    },
    "Haber Global": {
        "url": "https://haberglobal.com.tr/rss",
        "gorus": "Merkez / Bağımsız"
    },

    # --------------------------------------------------------------------------
    # 3. MUHALIF / ELESTIREL (12 Kaynak)
    # --------------------------------------------------------------------------
    "Sözcü": {
        "url": "https://www.sozcu.com.tr/rss/gundem.xml",
        "gorus": "Muhalif / Eleştirel"
    },
    "Cumhuriyet": {
        "url": "https://www.cumhuriyet.com.tr/rss",
        "gorus": "Muhalif / Eleştirel"
    },
    "BirGün": {
        "url": "https://www.birgun.net/xml/rss.xml",
        "gorus": "Muhalif / Eleştirel"
    },
    "Halk TV": {
        "url": "https://halktv.com.tr/rss",
        "gorus": "Muhalif / Eleştirel"
    },
    "Gazete Duvar": {
        "url": "https://www.gazeteduvar.com.tr/rss",
        "gorus": "Muhalif / Eleştirel"
    },
    "Diken": {
        "url": "https://www.diken.com.tr/feed/",
        "gorus": "Muhalif / Eleştirel"
    },
    "Karar": {
        "url": "https://www.karar.com/rss",
        "gorus": "Muhalif / Eleştirel"
    },
    "Yeniçağ": {
        "url": "https://www.yenicaggazetesi.com.tr/rss",
        "gorus": "Muhalif / Eleştirel"
    },
    "Evrensel": {
        "url": "https://www.evrensel.net/rss/haber.xml",
        "gorus": "Muhalif / Eleştirel"
    },
    "Gerçek Gündem": {
        "url": "https://www.gercekgundem.com/rss",
        "gorus": "Muhalif / Eleştirel"
    },
    "Kısa Dalga": {
        "url": "https://kisadalga.net/rss",
        "gorus": "Muhalif / Eleştirel"
    },
    "Tele1": {
        "url": "https://tele1.com.tr/rss",
        "gorus": "Muhalif / Eleştirel"
    }
}

# ==============================================================================
# GECMIS VERILERI KONTROL ETME (MUKERRER HABERLERI ONLEME)
# ==============================================================================
islenen_linkler = set()
try:
    df_eski = pd.read_csv("analizli_haber_veriseti.csv")
    if "Link" in df_eski.columns:
        islenen_linkler = set(df_eski["Link"].dropna().tolist())
except FileNotFoundError:
    pass

toplanan_haberler = []

# ==============================================================================
# VERI CEKME VE AYIKLAMA DONGUSU
# ==============================================================================
print(f"Toplam {len(rss_kaynaklari)} kaynaktan haber cekimi baslatiliyor...")

for kaynak_adi, detay in rss_kaynaklari.items():
    url = detay["url"]
    gorus = detay["gorus"]
    
    try:
        # RSS feed parser cagrisi
        feed = feedparser.parse(url, request_headers=TARAYICI_BASLIGI)
        
        if not feed.entries:
            print(f"[{kaynak_adi}] UYARI: Besleme bos dondu veya erisilemedi ({url})")
            continue
            
        cekilen_sayisi = 0
        
        for entry in feed.entries[:KAYNAK_BASINA_HABER_LIMITI]:
            link = entry.link.strip() if hasattr(entry, 'link') and entry.link else ""
            
            # Eger bu haber daha once islendiyse atla
            if link and link in islenen_linkler:
                continue

            baslik = entry.title.strip() if hasattr(entry, 'title') and entry.title else ""
            if not baslik:
                continue

            ozet = ""
            if hasattr(entry, 'summary') and entry.summary:
                ozet = entry.summary.strip()
            elif hasattr(entry, 'description') and entry.description:
                ozet = entry.description.strip()

            gorsel_url = ""
            import re
            
            if hasattr(entry, 'media_content') and len(entry.media_content) > 0:
                for media in entry.media_content:
                    if 'url' in media and ('image' in media.get('medium', '') or media['url'].endswith(('.jpg', '.png', '.jpeg', '.webp'))):
                        gorsel_url = media['url']
                        break
            
            if not gorsel_url and hasattr(entry, 'links'):
                for e_link in entry.links:
                    if e_link.get('rel') == 'enclosure' and 'image' in e_link.get('type', ''):
                        gorsel_url = e_link.get('href')
                        break
            
            if not gorsel_url and ozet:
                match = re.search(r'<img[^>]+src="([^">]+)"', ozet)
                if match:
                    gorsel_url = match.group(1)

            tarih = ""
            if hasattr(entry, 'published') and entry.published:
                tarih = entry.published
            elif hasattr(entry, 'updated') and entry.updated:
                tarih = entry.updated
            else:
                tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            toplanan_haberler.append({
                "Kaynak": kaynak_adi,
                "Gorus_Acisi": gorus,
                "Tarih": tarih,
                "Baslik": baslik,
                "Ozet": ozet,
                "Link": link,
                "Gorsel_URL": gorsel_url
            })
            cekilen_sayisi += 1
            
        print(f"[{kaynak_adi}] {cekilen_sayisi} YENI haber basariyla alindi.")

    except Exception as e:
        print(f"[{kaynak_adi}] HATA OLUSTU: {e}")

# ==============================================================================
# VERILERI CSV DOSYASINA KAYDETME
# ==============================================================================
cikti_dosyasi = "haber_veriseti.csv"

if toplanan_haberler:
    df = pd.DataFrame(toplanan_haberler)
    df.to_csv(cikti_dosyasi, index=False, encoding="utf-8-sig")
    print("-" * 60)
    print(f"Islem tamamlandi. Toplam {len(toplanan_haberler)} YENI haber '{cikti_dosyasi}' dosyasina kaydedildi.")
    print("Gorus acisina gore dagilim:")
    print(df["Gorus_Acisi"].value_counts().to_string())
else:
    # Eski verilerin tekrar islenmemesi icin batch dosyasini bosaltiyoruz
    pd.DataFrame().to_csv(cikti_dosyasi, index=False)
    print("Yeni haber bulunamadi. İlgili veri seti bos olarak guncellendi.")