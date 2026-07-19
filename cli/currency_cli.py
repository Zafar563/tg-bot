import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from currency import get_usd_rate, parse_amount


def convert(text):
    amount = parse_amount(text)
    if amount is None or amount <= 0:
        print("Xato: Noto'g'ri summa. Musbat son kiriting (masalan: 150000).")
        return
    usd_rate = get_usd_rate()
    if not usd_rate:
        print("Xato: USD kursini olishda muammo. Keyinroq qayta urinib ko'ring.")
        return
    fmt_uzs  = f"{amount:,.0f}".replace(",", " ")
    fmt_usd  = f"{amount / usd_rate:,.2f}"
    fmt_rate = f"{usd_rate:,.2f}".replace(",", " ")
    print(f"\n--- Valyuta konvertori ---")
    print(f"Kiritilgan summa : {fmt_uzs} so'm")
    print(f"AQSH dollari     : {fmt_usd} $")
    print(f"Bugungi kurs     : 1 USD = {fmt_rate} so'm")
    print("(Kurs O'zbekiston Markaziy Banki API'sidan olindi.)")


if __name__ == "__main__":
    print("========================================")
    print("      Valyuta Konvertori (UZS->USD)     ")
    print("========================================")
    try:
        while True:
            text = input("\nSo'm miqdorini kiriting (masalan: 150000): ").strip()
            if not text:
                continue
            convert(text)
    except (KeyboardInterrupt, EOFError):
        print("\nXayr!")
        sys.exit(0)
