import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================================================================
# TARAFIZLIK TURKIYE - KULLANICI ARAYUZU (uygulama.py)
# ==============================================================================
st.set_page_config(
    page_title="Tarafsızlık Türkiye",
    layout="wide"
)

# ==============================================================================
# METINLER VE CEVIRILER
# ==============================================================================
TEXTS = {
    "title": {"tr": "Tarafsızlık Türkiye", "en": "Tarafsızlık Türkiye"},
    "subtitle": {"tr": "Türkiye medyasının olaylara editoryal bakış açısını analiz eden tarafsız platform.", "en": "An objective platform analyzing the editorial perspectives of Turkish media on current events."},
    "what_is_it": {
        "tr": "<b>Nedir?</b> Yapay zeka ile 36 ulusal kaynağı tarayıp gruplayan analiz platformu. Renkli çubuklar haberin hangi editoryal kutup tarafından sahiplenildiğini, <b>'Kör Noktalar'</b> ise bir tarafın kasten görmezden geldiği (sansürlediği) gündemleri gösterir.",
        "en": "<b>What is it?</b> AI-powered media analysis scanning 36 national sources. Colored bars show coverage ratio by editorial poles, while <b>'Blindspots'</b> on the left reveal crucial stories deliberately ignored by one side."
    },
    "filter": {"tr": "Konu Filtresi", "en": "Topic Filter"},
    "time_filter": {"tr": "Zaman Aralığı", "en": "Timeframe"},
    "time_24h": {"tr": "Bugün (24s)", "en": "Today (24h)"},
    "time_7d": {"tr": "Bu Hafta (7g)", "en": "This Week (7d)"},
    "time_30d": {"tr": "Bu Ay (30g)", "en": "This Month (30d)"},
    "all_news": {"tr": "Tüm Gündem", "en": "All Stories"},
    "agenda": {"tr": "Gündem", "en": "Top Stories"},
    "inspect": {"tr": "İncele", "en": "Inspect"},
    "inspect_details": {"tr": "İncele", "en": "Inspect"},
    "blindspots": {"tr": "Kör Noktalar", "en": "Blindspots"},
    "blindspots_desc": {"tr": "Bir kutbun (Sağ/Sol) kasıtlı olarak görmezden geldiği veya %10'dan az yer verdiği kritik haberler.", "en": "Crucial stories deliberately ignored or given <10% coverage by one editorial pole."},
    "missed_left": {"tr": "Solun Kaçırdıkları", "en": "Missed by Left"},
    "missed_right": {"tr": "Sağın Kaçırdıkları", "en": "Missed by Right"},
    "left_cov": {"tr": "Sol Kapsamı", "en": "Left Cov."},
    "right_cov": {"tr": "Sağ Kapsamı", "en": "Right Cov."},
    "more_blindspots": {"tr": "Diğer Kör Noktaları Gör", "en": "View More Blindspots"},
    "no_left_miss": {"tr": "Şu an sol basının < %10 atladığı gündem yok.", "en": "Currently no major blindspots for the Left media."},
    "no_right_miss": {"tr": "Şu an sağ basının < %10 atladığı gündem yok.", "en": "Currently no major blindspots for the Right media."},
    "view_all_sources": {"tr": "Tüm Kaynakları Gör", "en": "View All Sources"},
    "headlines": {"tr": "Manşetler", "en": "Headlines"},
    "neutral_summary": {"tr": "Tarafsız Özet", "en": "Neutral Summary"},
    "info_btn": {"tr": "Bilgi", "en": "Info"}
}

# --- RENK VE GORUS PALETI ---
POLARITY_EN = {
    "Muhalif / Eleştirel": "Left / Opposition",
    "Merkez / Bağımsız": "Center / Independent",
    "Muhafazakar / İktidar Çizgisi": "Right / Pro-Gov"
}

TAGS_EN = {
    "#İçPolitika": "#DomesticPolitics", "#DışPolitika": "#ForeignPolicy",
    "#EkonomiVePiyasalar": "#Economy&Markets", "#EnflasyonVeGeçim": "#Inflation&Living",
    "#AdaletVeYargı": "#Justice&Law", "#AnayasaVeMeclis": "#Constitution&Parliament",
    "#SeçimVePartiler": "#Elections&Parties", "#GüvenlikVeTerör": "#Security&Terrorism",
    "#SavunmaSanayii": "#DefenseIndustry", "#GöçVeSığınmacılar": "#Migration&Refugees",
    "#Eğitim": "#Education", "#Sağlık": "#Health", "#KadınVeÇocukHakları": "#Women&ChildrenRights",
    "#İnsanHaklarıVeHukuk": "#HumanRights", "#MedyaVeİfadeÖzgürlüğü": "#Media&FreeSpeech",
    "#YerelYönetimler": "#LocalGov", "#ÇevreVeİklim": "#Environment&Climate",
    "#DepremVeAfet": "#Earthquake&Disaster"
}

RENK_HARITASI = {
    "Muhalif / Eleştirel": "#d62728",
    "Merkez / Bağımsız": "#d3d3d3",
    "Muhafazakar / İktidar Çizgisi": "#ff7f0e"
}
RENK_HARITASI_EN = {POLARITY_EN[k]: v for k, v in RENK_HARITASI.items()}

VARSAYILAN_GORSEL = "https://images.unsplash.com/photo-1585829365295-ab7cd400c167?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"

# ==============================================================================
# UST BILGI VE DIL AYARLARI 
# ==============================================================================
col_t, col_lang = st.columns([8.5, 1.5], gap="small", vertical_alignment="bottom")

with col_lang:
    secilen_dil = st.pills("Lang", ["🇹🇷 TR", "🇬🇧 EN"], default="🇹🇷 TR", label_visibility="collapsed")
    is_en = secilen_dil == "🇬🇧 EN"
    lang = "en" if is_en else "tr"

with col_t:
    html_title = f"""
    <div style='display: flex; align-items: baseline; flex-wrap: wrap; gap: 15px; margin-bottom: 5px;'>
        <h2 style='margin: 0; padding: 0;'>{TEXTS['title'][lang]}</h2>
        <span style='color: #888; font-size: 1.05em; font-style: italic;'>{TEXTS['subtitle'][lang]}</span>
    </div>
    """
    st.markdown(html_title, unsafe_allow_html=True)

# Başlığın hemen altı - Nedir metni
html_nedir = f"<div style='color: #ccc; font-size: 0.95em; margin-bottom: 25px; line-height: 1.5;'>{TEXTS['what_is_it'][lang]}</div>"
if is_en:
    html_nedir += "<div style='color: #999; font-size: 0.85em; font-style: italic; margin-top: -15px; margin-bottom: 25px;'>Note: As this is a beta version, news headlines and summaries are kept in their original Turkish language.</div>"

st.markdown(html_nedir, unsafe_allow_html=True)

# ==============================================================================
# VERI YUKLEME
# ==============================================================================
@st.cache_data
def veri_yukle():
    try:
        df = pd.read_csv("analizli_haber_veriseti.csv")
        df = df[df["Grup_Basligi"].notna()]
        df = df[~df["Grup_Basligi"].isin(["Grup Yok", "Ilgisiz", "İlgisiz"])]
        if "Gorsel_URL" not in df.columns:
            df["Gorsel_URL"] = ""
        if "Tarih" in df.columns:
            df["Analiz_Tarihi"] = pd.to_datetime(df["Tarih"], errors="coerce", utc=True).dt.tz_localize(None)
        elif "Analiz_Tarihi" not in df.columns:
            df["Analiz_Tarihi"] = pd.Timestamp.now()
        else:
            df["Analiz_Tarihi"] = pd.to_datetime(df["Analiz_Tarihi"], errors="coerce", utc=True).dt.tz_localize(None)
        return df
    except FileNotFoundError:
        return pd.DataFrame()

df_ham = veri_yukle()

if df_ham.empty:
    st.error("Veri bulunamadi. Lutfen once veri_cekici.py ve ai_analiz.py scriptlerini calistirin.")
    st.stop()

# ==============================================================================
# ZAMAN VE KONU FILTRELERI (Tek Satirda Yan Yana)
# ==============================================================================
col_zaman, col_konu = st.columns([1.5, 4.5], vertical_alignment="bottom")

with col_zaman:
    zaman_secenekleri = [TEXTS["time_24h"][lang], TEXTS["time_7d"][lang], TEXTS["time_30d"][lang]]
    secilen_zaman = st.pills(TEXTS["time_filter"][lang], zaman_secenekleri, default=zaman_secenekleri[0])

# Tarihe gore filtreleme
su_an = pd.Timestamp.now()
if secilen_zaman == TEXTS["time_7d"][lang]:
    df = df_ham[df_ham["Analiz_Tarihi"] >= (su_an - pd.Timedelta(days=7))]
elif secilen_zaman == TEXTS["time_30d"][lang]:
    df = df_ham[df_ham["Analiz_Tarihi"] >= (su_an - pd.Timedelta(days=30))]
else:
    # 24 saat (Bugun) secenegi
    df = df_ham[df_ham["Analiz_Tarihi"] >= (su_an - pd.Timedelta(days=1))]

zaman_etiketi = secilen_zaman if secilen_zaman else TEXTS["time_24h"][lang]
baslik_eki = f" <span style='color:#777; font-size:0.6em; font-weight:normal;'>{zaman_etiketi}</span>"

# Gruplama (Sadece zaman filtresine giren data)
gruplar_istatistik = []
for grup_adi, grup_verisi in df.groupby("Grup_Basligi"):
    # Yeni: Kaynaklara gore tekillestirilmis sayilar
    muhalif = grup_verisi[grup_verisi["Gorus_Acisi"] == "Muhalif / Eleştirel"]["Kaynak"].nunique()
    merkez = grup_verisi[grup_verisi["Gorus_Acisi"] == "Merkez / Bağımsız"]["Kaynak"].nunique()
    muhafazakar = grup_verisi[grup_verisi["Gorus_Acisi"] == "Muhafazakar / İktidar Çizgisi"]["Kaynak"].nunique()
    toplam_essiz = muhalif + merkez + muhafazakar
    
    gorseller = grup_verisi[grup_verisi["Gorsel_URL"].notna() & (grup_verisi["Gorsel_URL"] != "")]["Gorsel_URL"].tolist()
    gorsel = gorseller[0] if gorseller else VARSAYILAN_GORSEL
    etiketler = str(grup_verisi.iloc[0]["Etiketler"])
    
    grup_ozeti = grup_verisi.iloc[0]["Grup_Ozeti"] if "Grup_Ozeti" in grup_verisi.columns else ""
    
    gruplar_istatistik.append({
        "Grup_Basligi": grup_adi,
        "Toplam": toplam_essiz,
        "Gercek_Toplam": len(grup_verisi),
        "Muhalif": muhalif,
        "Merkez": merkez,
        "Muhafazakar": muhafazakar,
        "Gorsel": gorsel,
        "Etiketler": etiketler,
        "Grup_Ozeti": grup_ozeti,
        "Veri": grup_verisi
    })

sirali_gruplar = sorted(gruplar_istatistik, key=lambda x: x["Toplam"], reverse=True)

with col_konu:
    etiket_sayilari = {}
    for h in sirali_gruplar:
        for e in h["Etiketler"].split(","):
            temiz = e.strip()
            if temiz.startswith("#"):
                gorunen_etiket = TAGS_EN.get(temiz, temiz) if is_en else temiz
                etiket_sayilari[gorunen_etiket] = etiket_sayilari.get(gorunen_etiket, 0) + h["Toplam"]
                if "original" not in h:
                    h["original"] = []
                h["original"].append(gorunen_etiket)

    populer_etiketler = sorted(etiket_sayilari.items(), key=lambda x: x[1], reverse=True)
    tum_secenek = TEXTS["all_news"][lang]
    secenekler = [tum_secenek] + [e[0] for e in populer_etiketler[:8]]

    secilen_etiket = st.pills(TEXTS["filter"][lang], secenekler, default=tum_secenek)

if not secilen_etiket or secilen_etiket == tum_secenek:
    gosterilecek_gruplar = sirali_gruplar
else:
    gosterilecek_gruplar = [h for h in sirali_gruplar if secilen_etiket in h.get("original", [])]

st.write("---") # Filtreler ile Haberlerin arasini ayiran tek ince cizgi

# ==============================================================================
# YARDIMCI FONKSIYONLAR
# ==============================================================================
def cizgi_cubuk_olustur(muhalif, merkez, muhafazakar, toplam):
    p_muh = (muhalif / toplam) * 100 if toplam > 0 else 0
    p_mer = (merkez / toplam) * 100 if toplam > 0 else 0
    p_muhaf = (muhafazakar / toplam) * 100 if toplam > 0 else 0
    
    t_muh = f"Left: {p_muh:.0f}%" if is_en else f"Muhalif: %{p_muh:.0f}"
    t_mer = f"Center: {p_mer:.0f}%" if is_en else f"Merkez: %{p_mer:.0f}"
    t_muhaf = f"Right: {p_muhaf:.0f}%" if is_en else f"Muhafazakar: %{p_muhaf:.0f}"

    html = f"""
    <div style="display: flex; height: 12px; width: 100%; border-radius: 6px; overflow: hidden; margin-top: 5px; margin-bottom: 10px; border: 1px solid #555;">
        <div style="width: {p_muh}%; background-color: {RENK_HARITASI['Muhalif / Eleştirel']};" title="{t_muh}"></div>
        <div style="width: {p_mer}%; background-color: {RENK_HARITASI['Merkez / Bağımsız']};" title="{t_mer}"></div>
        <div style="width: {p_muhaf}%; background-color: {RENK_HARITASI['Muhafazakar / İktidar Çizgisi']};" title="{t_muhaf}"></div>
    </div>
    """
    return html

def haber_detayi_goster(grup_istatistik, anahtar=""):
    verisi = grup_istatistik["Veri"]
    toplam = grup_istatistik["Toplam"]
    grup_ozeti = grup_istatistik.get("Grup_Ozeti", "")
    
    if grup_ozeti:
        prefix = TEXTS["neutral_summary"][lang]
        st.markdown(f"<div style='background-color: #2e2e2e; padding: 12px; border-radius: 6px; margin-bottom: 15px; border-left: 3px solid #777; font-size: 0.95em;'><b>{prefix}:</b> {grup_ozeti}</div>", unsafe_allow_html=True)
    
    gorus_dagilimi = verisi["Gorus_Acisi"].value_counts().reset_index()
    if is_en:
        gorus_dagilimi["Gorus_Acisi"] = gorus_dagilimi["Gorus_Acisi"].map(POLARITY_EN)
        harita = RENK_HARITASI_EN
        col_name = "Editorial Stance"
    else:
        harita = RENK_HARITASI
        col_name = "Editoryal Duruş"
        
    gorus_dagilimi.columns = [col_name, "Count" if is_en else "Haber Sayısı"]
    
    fig = px.pie(
        gorus_dagilimi, 
        names=col_name, 
        values="Count" if is_en else "Haber Sayısı", 
        hole=0.5,
        color=col_name,
        color_discrete_map=harita
    )
    center_text = f"{toplam}<br>Sources" if is_en else f"{toplam}<br>Kaynak"
    fig.update_layout(
        annotations=[dict(text=center_text, x=0.5, y=0.5, font_size=20, showarrow=False)],
        margin=dict(t=20, b=10, l=20, r=20),
        height=320,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        )
    )
    st.plotly_chart(fig, use_container_width=True, key=f"pie_{anahtar}")
    
    with st.popover(TEXTS["view_all_sources"][lang], use_container_width=True):
        st.markdown(f"#### {TEXTS['headlines'][lang]}")
        for _, satir in verisi.iterrows():
            gorus_etiketi = POLARITY_EN[satir["Gorus_Acisi"]] if is_en else satir["Gorus_Acisi"]
            kaynak = satir["Kaynak"]
            baslik = satir["Baslik"]
            link = satir["Link"]
            renk = RENK_HARITASI.get(satir["Gorus_Acisi"], "#fff")
            
            if link:
                st.markdown(f"- <span style='color:{renk}; font-weight:bold;'>[{kaynak}]</span>: [{baslik}]({link})", unsafe_allow_html=True)
            else:
                st.markdown(f"- <span style='color:{renk}; font-weight:bold;'>[{kaynak}]</span>: {baslik}", unsafe_allow_html=True)

def gorsel_kutu(gorsel_url, yukseklik="300px"):
    html = f"""
    <div style="width:100%; height:{yukseklik}; border-radius:6px; overflow:hidden; margin-bottom:8px; background-color:#1e1e1e;">
        <img src="{gorsel_url}" style="width:100%; height:100%; object-fit:cover;" onerror="this.src='{VARSAYILAN_GORSEL}'">
    </div>
    """
    return html

# ==============================================================================
# ANA EKRAN: GUNDEM VE KOR NOKTALAR
# ==============================================================================
col_sag, col_ana = st.columns([1, 3], gap="large")

with col_ana:
    # margin-top: 0 hizalama hatasini gidermek icin eklendi
    st.markdown(f"<h3 style='margin-top:0; padding-top:0;'>{TEXTS['agenda'][lang]}{baslik_eki}</h3>", unsafe_allow_html=True)
    
    if len(gosterilecek_gruplar) > 0:
        c1, c2, c3 = st.columns(3, gap="medium")
        
        if len(gosterilecek_gruplar) > 0:
            h1 = gosterilecek_gruplar[0]
            with c1:
                st.markdown(gorsel_kutu(h1["Gorsel"], yukseklik="160px"), unsafe_allow_html=True)
                st.markdown(f"<h5 style='margin-bottom:0;'>{h1['Grup_Basligi']}</h5>", unsafe_allow_html=True)
                st.markdown(cizgi_cubuk_olustur(h1["Muhalif"], h1["Merkez"], h1["Muhafazakar"], h1["Toplam"]), unsafe_allow_html=True)
                with st.expander(TEXTS["inspect_details"][lang]):
                    haber_detayi_goster(h1, f"gundem_{h1['Grup_Basligi']}")
                    
        if len(gosterilecek_gruplar) > 1:
            h2 = gosterilecek_gruplar[1]
            with c2:
                st.markdown(gorsel_kutu(h2["Gorsel"], yukseklik="160px"), unsafe_allow_html=True)
                st.markdown(f"<h5 style='margin-bottom:0;'>{h2['Grup_Basligi']}</h5>", unsafe_allow_html=True)
                st.markdown(cizgi_cubuk_olustur(h2["Muhalif"], h2["Merkez"], h2["Muhafazakar"], h2["Toplam"]), unsafe_allow_html=True)
                with st.expander(TEXTS["inspect"][lang]):
                    haber_detayi_goster(h2, f"gundem_{h2['Grup_Basligi']}")
                    
        if len(gosterilecek_gruplar) > 2:
            h3 = gosterilecek_gruplar[2]
            with c3:
                st.markdown(gorsel_kutu(h3["Gorsel"], yukseklik="160px"), unsafe_allow_html=True)
                st.markdown(f"<h5 style='margin-bottom:0;'>{h3['Grup_Basligi']}</h5>", unsafe_allow_html=True)
                st.markdown(cizgi_cubuk_olustur(h3["Muhalif"], h3["Merkez"], h3["Muhafazakar"], h3["Toplam"]), unsafe_allow_html=True)
                with st.expander(TEXTS["inspect"][lang]):
                    haber_detayi_goster(h3, f"gundem_{h3['Grup_Basligi']}")
                    
        st.write("---")
        
    if len(gosterilecek_gruplar) > 3:
        for i, h in enumerate(gosterilecek_gruplar[3:]):
            st.markdown(f"#### {h['Grup_Basligi']}")
            st.markdown(cizgi_cubuk_olustur(h["Muhalif"], h["Merkez"], h["Muhafazakar"], h["Toplam"]), unsafe_allow_html=True)
            with st.expander(TEXTS["inspect"][lang]):
                haber_detayi_goster(h, f"gundem_liste_{i}_{h['Grup_Basligi']}")
            st.write("")

def kor_noktalari_listele(kn_listesi, renk_kodu, dil_metni, p_metni, taraf_prefix=""):
    ilk = True
    gosterilen_sayi = 0
    for hk in kn_listesi[:2]:
        if ilk:
            st.markdown(gorsel_kutu(hk["Gorsel"], yukseklik="100px"), unsafe_allow_html=True)
            ilk = False
        st.markdown(f"**{hk['Grup_Basligi']}**")
        st.markdown(cizgi_cubuk_olustur(hk["Muhalif"], hk["Merkez"], hk["Muhafazakar"], hk["Toplam"]), unsafe_allow_html=True)
        st.markdown(f"<span style='font-size:0.85em; color:{renk_kodu}; font-weight:bold;'>%{hk['KorNokta_Oran']} {p_metni}</span>", unsafe_allow_html=True)
        with st.expander(TEXTS["inspect_details"][lang]):
            haber_detayi_goster(hk, f"kn_ilk_{taraf_prefix}_{hk['Grup_Basligi']}")
        st.write("---")
        gosterilen_sayi += 1
        
    if len(kn_listesi) > 2:
        with st.expander(f"{TEXTS['more_blindspots'][lang]} (+{len(kn_listesi) - 2})"):
            for i, hk in enumerate(kn_listesi[2:]):
                st.markdown(f"**{hk['Grup_Basligi']}**")
                st.markdown(cizgi_cubuk_olustur(hk["Muhalif"], hk["Merkez"], hk["Muhafazakar"], hk["Toplam"]), unsafe_allow_html=True)
                st.markdown(f"<span style='font-size:0.85em; color:{renk_kodu}; font-weight:bold;'>%{hk['KorNokta_Oran']} {p_metni}</span>", unsafe_allow_html=True)
                with st.expander(TEXTS["inspect_details"][lang]):
                    haber_detayi_goster(hk, f"kn_diger_{taraf_prefix}_{i}_{hk['Grup_Basligi']}")
                st.write("---")

with col_sag:
    # margin-top: 0 hizalama hatasini gidermek icin eklendi
    st.markdown(f"<h3 style='margin-top:0; padding-top:0;'>{TEXTS['blindspots'][lang]}{baslik_eki}</h3>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size:0.9em; color:#bbb;'>{TEXTS['blindspots_desc'][lang]}</span>", unsafe_allow_html=True)
    st.write("")
    
    muhalif_kacirmis = []
    muhafazakar_kacirmis = []
    
    for h in gosterilecek_gruplar:
        p_muh = int((h["Muhalif"] / h["Toplam"]) * 100) if h["Toplam"] > 0 else 0
        p_sag = int((h["Muhafazakar"] / h["Toplam"]) * 100) if h["Toplam"] > 0 else 0
        p_mer = int((h["Merkez"] / h["Toplam"]) * 100) if h["Toplam"] > 0 else 0
        
        if p_muh <= 10 and (p_sag + p_mer) > 20:
            hk = h.copy()
            hk["KorNokta_Oran"] = p_muh
            muhalif_kacirmis.append(hk)
            
        elif p_sag <= 10 and (p_muh + p_mer) > 20:
            hk = h.copy()
            hk["KorNokta_Oran"] = p_sag
            muhafazakar_kacirmis.append(hk)
    
    header_left = "Left's" if is_en else "Solun"
    st.markdown(f"#### <span style='color:{RENK_HARITASI['Muhalif / Eleştirel']}'>{header_left}</span> {TEXTS['missed_left'][lang].split()[-1]}", unsafe_allow_html=True)
    
    if muhalif_kacirmis:
        kor_noktalari_listele(muhalif_kacirmis, RENK_HARITASI['Muhalif / Eleştirel'], lang, TEXTS['left_cov'][lang], "sol")
    else:
        st.info(TEXTS["no_left_miss"][lang])
        
    st.write("")
    
    header_right = "Right's" if is_en else "Sağın"
    st.markdown(f"#### <span style='color:{RENK_HARITASI['Muhafazakar / İktidar Çizgisi']}'>{header_right}</span> {TEXTS['missed_right'][lang].split()[-1]}", unsafe_allow_html=True)
    
    if muhafazakar_kacirmis:
         kor_noktalari_listele(muhafazakar_kacirmis, RENK_HARITASI['Muhafazakar / İktidar Çizgisi'], lang, TEXTS['right_cov'][lang], "sag")
    else:
        st.info(TEXTS["no_right_miss"][lang])

# ==============================================================================
# FOOTER (ALTYAPI VE YASAL NOTLAR)
# ==============================================================================
st.markdown("---")
footer_text = "Data is automatically aggregated from 36 national RSS feeds and clustered via Google Gemini AI. Developed for media transparency." if is_en else "Veriler 36 ulusal haber kaynağından RSS ile anlık toplanmakta ve Google Gemini Yapay Zekası ile gruplanmaktadır. Medya şeffaflığı için geliştirilmiştir."
disclaimer = "We do not track user data (No cookies/GDPR consent required). News content belongs to their respective publishers." if is_en else "Bu platform kullanıcı verisi toplamaz (Çerez/KVKK onayı gerektirmez). Haber içeriklerinin telif hakları ilgili yayıncılara aittir."
st.markdown(f"<div style='text-align: center; color: #888; font-size: 0.9em;'>{footer_text}<br><i>{disclaimer}</i><br><br><b>Tarafsızlık Türkiye</b> &copy; 2026</div>", unsafe_allow_html=True)