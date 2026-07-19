import httpx

REGION_MAP = {
    "tashkent": "Toshkent", "samarkand": "Samarqand", "bukhara": "Buxoro",
    "andijan": "Andijon", "namangan": "Namangan", "fergana": "Farg'ona",
    "jizzakh": "Jizzax", "navoiy": "Navoiy", "nukus": "Nukus",
    "qarshi": "Qarshi", "termez": "Termiz", "gulistan": "Guliston",
    "khiva": "Xiva", "urgench": "Urganch", "kokand": "Qo'qon"
}

ALADHAN_MAP = {
    "Toshkent": "Tashkent", "Samarqand": "Samarkand", "Buxoro": "Bukhara",
    "Andijon": "Andijan", "Namangan": "Namangan", "Farg'ona": "Fergana",
    "Jizzax": "Jizzakh", "Navoiy": "Navoiy", "Nukus": "Nukus",
    "Qarshi": "Qarshi", "Termiz": "Termez", "Guliston": "Gulistan",
    "Xiva": "Khiva", "Urganch": "Urgench", "Qo'qon": "Kokand"
}

WEEKDAYS_UZ = {
    "Monday": "Dushanba", "Tuesday": "Seshanba", "Wednesday": "Chorshanba",
    "Thursday": "Payshanba", "Friday": "Juma", "Saturday": "Shanba", "Sunday": "Yakshanba"
}


def get_prayer_times(region):
    mapped = REGION_MAP.get(region.strip().lower(), region.strip())

    # 1. Try islomapi.uz
    try:
        with httpx.Client() as client:
            r = client.get(f"https://islomapi.uz/api/present/day?region={mapped}", timeout=10)
        if r.status_code == 200:
            data = r.json()
            data["source"] = "islom.uz"
            return data
    except Exception:
        pass

    # 2. Fallback to Aladhan
    city = ALADHAN_MAP.get(mapped, mapped)
    try:
        with httpx.Client() as client:
            r = client.get(
                f"https://api.aladhan.com/v1/timingsByCity?city={city}&country=Uzbekistan&method=3",
                follow_redirects=True, timeout=10
            )
        if r.status_code == 200:
            node = r.json().get("data", {})
            timings = node.get("timings", {})
            date_node = node.get("date", {})
            eng_day = date_node.get("gregorian", {}).get("weekday", {}).get("en", "")
            return {
                "region": mapped,
                "date": date_node.get("readable", ""),
                "weekday": WEEKDAYS_UZ.get(eng_day, eng_day),
                "times": {
                    "tong_saharlik": timings.get("Fajr"),
                    "quyosh": timings.get("Sunrise"),
                    "peshin": timings.get("Dhuhr"),
                    "asr": timings.get("Asr"),
                    "shom_iftor": timings.get("Maghrib"),
                    "xufton": timings.get("Isha")
                },
                "source": "Aladhan API"
            }
    except Exception:
        pass

    return None


def format_prayer_times(data):
    if not data:
        return None
    times = data.get("times", {})
    source = data.get("source", "islom.uz")
    src_text = "islom.uz portalidan olindi." if source == "islom.uz" else "zaxira Aladhan tizimidan olindi."
    return (
        f"🕋 **Namoz Vaqtlari — {data.get('region')}**\n"
        f"📅 **Sana:** {data.get('date')} ({data.get('weekday')})\n\n"
        f"🏙 **Tong (Saharlik):** {times.get('tong_saharlik')}\n"
        f"🌅 **Quyosh:** {times.get('quyosh')}\n"
        f"☀️ **Peshin:** {times.get('peshin')}\n"
        f"🌇 **Asr:** {times.get('asr')}\n"
        f"🌆 **Shom (Iftor):** {times.get('shom_iftor')}\n"
        f"🌃 **Xufton:** {times.get('xufton')}\n\n"
        f"ℹ️ _Ma'lumotlar {src_text}_"
    )
