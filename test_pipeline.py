import pandas as pd

def test_unique_source_counting():
    # Sahte veri
    data = {
        "Grup_Basligi": ["Test Konu"] * 4,
        "Gorus_Acisi": ["Muhalif / Eleştirel", "Muhalif / Eleştirel", "Merkez / Bağımsız", "Muhafazakar / İktidar Çizgisi"],
        "Kaynak": ["Sözcü", "Sözcü", "Habertürk", "Sabah"],
        "Gorsel_URL": ["", "", "", ""],
        "Etiketler": ["#Test", "#Test", "#Test", "#Test"],
        "Grup_Ozeti": ["Test Ozet"] * 4
    }
    df = pd.DataFrame(data)
    
    # 4 haber var, ama 3 benzersiz kaynak var (Sözcü iki defa geciyor)
    for grup_adi, grup_verisi in df.groupby("Grup_Basligi"):
        muhalif = grup_verisi[grup_verisi["Gorus_Acisi"] == "Muhalif / Eleştirel"]["Kaynak"].nunique()
        merkez = grup_verisi[grup_verisi["Gorus_Acisi"] == "Merkez / Bağımsız"]["Kaynak"].nunique()
        muhafazakar = grup_verisi[grup_verisi["Gorus_Acisi"] == "Muhafazakar / İktidar Çizgisi"]["Kaynak"].nunique()
        
        assert muhalif == 1, f"Expected 1 unique Muhalif source, got {muhalif}"
        assert merkez == 1, f"Expected 1 unique Merkez source, got {merkez}"
        assert muhafazakar == 1, f"Expected 1 unique Muhafazakar source, got {muhafazakar}"
        assert (muhalif + merkez + muhafazakar) == 3, "Total unique sources should be 3"
        print("Unique source counting test passed!")

def test_date_parsing_fallback():
    # Sahte veri - Karisik offset olan ve olmayan tarihler
    data = {
        "Tarih": ["2026-10-02 12:00:00", "2026-10-02T12:00:00+03:00", "Hatalı Tarih"]
    }
    df = pd.DataFrame(data)
    
    # utc=True ve tz_localize(None) testi
    df["Analiz_Tarihi"] = pd.to_datetime(df["Tarih"], errors="coerce", utc=True).dt.tz_localize(None)
    
    # Hatalı olan NaT olmalı
    assert pd.isna(df.iloc[2]["Analiz_Tarihi"]), "Invalid date should parse as NaT"
    
    # Kalanların type'ı offset-naive datetime64 olmalı (kıyaslanabilmeli)
    su_an = pd.Timestamp.now()
    try:
        fark = su_an - df.iloc[0]["Analiz_Tarihi"]
        assert fark is not None
        print("Date parsing and comparison test passed!")
    except TypeError:
        raise Exception("Date comparison failed due to offset-naive / offset-aware mixup")

def test_xss_prevention():
    import html
    test_str = "<script>alert(1)</script>"
    escaped_str = html.escape(test_str)
    assert "<script>" not in escaped_str, "XSS not escaped properly"
    print("XSS prevention test passed!")

if __name__ == "__main__":
    test_unique_source_counting()
    test_date_parsing_fallback()
    test_xss_prevention()

