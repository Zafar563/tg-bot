import httpx

def get_usd_rate():
    url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
    try:
        with httpx.Client() as client:
            response = client.get(url, timeout=10)
        if response.status_code != 200:
            return None
        for item in response.json():
            if item.get("Ccy") == "USD":
                return float(item.get("Rate"))
        return None
    except Exception:
        return None


def parse_amount(text):
    clean = text.lower().replace("so'm", "").replace("som", "").replace("uzs", "").strip()
    clean = clean.replace(" ", "").replace(",", "")
    try:
        return float(clean) if "." in clean else int(clean)
    except ValueError:
        return None


def is_numeric_amount(text):
    val = parse_amount(text)
    return val is not None and val > 0


def convert_uzs_to_usd(amount_uzs):
    usd_rate = get_usd_rate()
    if not usd_rate:
        return "❌ USD kursini olishda xatolik yuz berdi. Iltimos keyinroq qaytadan urinib ko'ring."
    amount_usd = amount_uzs / usd_rate
    fmt_uzs  = f"{amount_uzs:,.2f}".replace(",", " ").replace(".00", "")
    fmt_usd  = f"{amount_usd:,.2f}".replace(",", " ")
    fmt_rate = f"{usd_rate:,.2f}".replace(",", " ")
    return (
        f"🧮 **Valyuta konvertori (UZS ➡️ USD)**\n\n"
        f"💵 **Kiritilgan summa:** {fmt_uzs} so'm\n"
        f"🇺🇸 **AQSH dollari:** {fmt_usd} $\n\n"
        f"📈 **Bugungi rasmiy kurs:** 1 USD = {fmt_rate} so'm\n"
        f"ℹ️ _Kurs O'zbekiston Respublikasi Markaziy Banki API'sidan olindi._"
    )
