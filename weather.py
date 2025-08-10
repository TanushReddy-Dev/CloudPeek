import requests

API_KEY = "9c0d80ecdb7fe798030d665461be9762"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

WEATHER_ICONS = {
    "clear": "☀️",
    "clouds": "☁️",
    "rain": "🌧️",
    "drizzle": "🌦️",
    "thunderstorm": "⛈️",
    "snow": "❄️",
    "mist": "🌫️",
    "fog": "🌫️",
    "haze": "🌫️"
}


def get_weather():
    city = input("Enter city name: ").strip()
    params = {"q": city, "appid": API_KEY, "units": "metric"}

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("cod") != 200:
        print(f"Error: {data.get('message', 'City not found or API error')}")
    else:
        weather_main = data["weather"][0]["main"].lower()
        weather_desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        icon = WEATHER_ICONS.get(weather_main, "")

        print(f"\nWeather in {city}:")
        print(f"Condition: {weather_desc} {icon}")
        print(f"Temperature: {temp}°C 🌡️")
        print(f"Humidity: {humidity}% 💧")
        print(f"Wind Speed: {wind_speed} m/s 🌬️")


if __name__ == "__main__":
    get_weather()
