import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx

API_KEY = "9e8d4bb64eb8b8161a1df865bdee0707"


def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=en"
        with httpx.Client() as client:
            r = client.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            print(f"\n--- Ob-havo: {city.title()} ---")
            print(f"Holat    : {data['weather'][0]['description'].capitalize()}")
            print(f"Harorat  : {data['main']['temp']}°C  (his: {data['main']['feels_like']}°C)")
            print(f"Namlik   : {data['main']['humidity']}%")
            print(f"Shamol   : {data['wind']['speed']} m/s")
            print(f"Bosim    : {data['main']['pressure']} hPa")
        elif r.status_code == 404:
            print("Xato: Shahar topilmadi. Nomni tekshiring.")
        elif r.status_code == 401:
            print("Xato: API kalit faol emas yoki noto'g'ri.")
        else:
            print(f"Xato: Server {r.status_code} qaytardi.")
    except Exception as e:
        print(f"Xato: {e}")


if __name__ == "__main__":
    print("========================================")
    print("         Ob-havo ma'lumoti              ")
    print("========================================")
    try:
        while True:
            name = input("\nIsmingizni kiriting: ").strip()
            if not name:
                continue
            city = input("Shahar nomini kiriting: ").strip()
            if not city:
                continue
            get_weather(city)
            print(f"\nSalom, {name}! Yana bir shaharni bilishni xohlaysizmi?")
    except (KeyboardInterrupt, EOFError):
        print("\nXayr!")
        sys.exit(0)
