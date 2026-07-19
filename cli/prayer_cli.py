import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prayer import get_prayer_times

REGIONS = [
    "Toshkent", "Samarqand", "Buxoro", "Andijon",
    "Namangan", "Farg'ona", "Xiva", "Qarshi",
    "Nukus", "Jizzax", "Navoiy", "Termiz"
]


def show_prayer(region):
    data = get_prayer_times(region)
    if not data:
        print(f"Xato: {region} bo'yicha namoz vaqtlarini yuklab bo'lmadi.")
        return
    times   = data.get("times", {})
    src_txt = "islom.uz" if data.get("source") == "islom.uz" else "Aladhan API (zaxira)"
    print(f"\n--- Namoz Vaqtlari: {region} ---")
    print(f"Sana     : {data.get('date')} ({data.get('weekday')})")
    print(f"Tong     : {times.get('tong_saharlik', '---')}")
    print(f"Quyosh   : {times.get('quyosh', '---')}")
    print(f"Peshin   : {times.get('peshin', '---')}")
    print(f"Asr      : {times.get('asr', '---')}")
    print(f"Shom     : {times.get('shom_iftor', '---')}")
    print(f"Xufton   : {times.get('xufton', '---')}")
    print(f"(Ma'lumot: {src_txt})")


if __name__ == "__main__":
    print("========================================")
    print("           Namoz Vaqtlari               ")
    print("========================================")
    print("Mavjud hududlar:")
    for i, r in enumerate(REGIONS, 1):
        print(f"  {i:2}. {r}")
    print("----------------------------------------")
    try:
        while True:
            text = input("\nHudud nomi yoki raqamini kiriting: ").strip()
            if not text:
                continue
            if text.isdigit():
                idx = int(text) - 1
                if 0 <= idx < len(REGIONS):
                    show_prayer(REGIONS[idx])
                else:
                    print(f"Xato: 1-{len(REGIONS)} oraligidagi raqam kiriting.")
            else:
                show_prayer(text)
    except (KeyboardInterrupt, EOFError):
        print("\nXayr!")
        sys.exit(0)
