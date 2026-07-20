
def format_openweathermap_report(data):
    name = data.get("name")
    country = data.get("sys", {}).get("country")
    temp = round(data.get("main", {}).get("temp"))
    feels_like = round(data.get("main", {}).get("feels_like"))
    humidity = data.get("main", {}).get("humidity")
    pressure = data.get("main", {}).get("pressure")
    wind_speed = data.get("wind", {}).get("speed")
    desc = data.get("weather", [{}])[0].get("description", "aniqlanmadi").capitalize()

    weather_id = data.get("weather", [{}])[0].get("id", 800)
    if weather_id == 800:
        emoji = "☀️"
    elif 200 <= weather_id < 300:
        emoji = "⛈"
    elif 300 <= weather_id < 500:
        emoji = "🌧"
    elif 500 <= weather_id < 600:
        emoji = "🌧"
    elif 600 <= weather_id < 700:
        emoji = "❄️"
    elif 700 <= weather_id < 800:
        emoji = "🌫"
    elif weather_id in (801, 802):
        emoji = "⛅️"
    else:
        emoji = "☁️"

    return (
        f"📍 **{name}, {country}** dagi ob-havo ma'lumotlari:\n\n"
        f"{emoji} **Holat:** {desc}\n"
        f"🌡 **Harorat:** {temp}°C\n"
        f"🤔 **Hissiyot:** {feels_like}°C\n"
        f"💧 **Namlik:** {humidity}%\n"
        f"💨 **Shamol tezligi:** {wind_speed} m/s\n"
        f"🌀 **Atmosfera bosimi:** {pressure} hPa\n\n"
        f"📅 _Ma'lumotlar hozirgi vaqt bo'yicha ko'rsatildi._"
    )
