import requests
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import io
import os
from datetime import datetime

API_KEY = "9c0d80ecdb7fe798030d665461be9762"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
LAST_CITY_FILE = "last_city.txt"

WEATHER_EMOJIS = {
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


def save_last_city(city):
    with open(LAST_CITY_FILE, "w") as f:
        f.write(city)


def load_last_city():
    if os.path.exists(LAST_CITY_FILE):
        with open(LAST_CITY_FILE, "r") as f:
            return f.read().strip()
    return ""


def unix_to_time(ts, tz_offset):
    return datetime.utcfromtimestamp(ts + tz_offset).strftime('%H:%M:%S')


def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showinfo("Input Error", "Please enter a city name.")
        return
    search_button.config(state=DISABLED)
    result_label.config(text="Fetching weather data...\nPlease wait...")
    app.update()

    params = {"q": city, "appid": API_KEY, "units": "metric"}

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()

        if data.get("cod") != 200:
            error_msg = data.get('message', 'City not found or API error')
            messagebox.showerror("Error", error_msg.capitalize())
            result_label.config(text="")
            search_button.config(state=NORMAL)
            return

        weather_main = data["weather"][0]["main"].lower()
        weather_desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        pressure = data["main"].get("pressure", "N/A")
        sunrise = unix_to_time(data["sys"]["sunrise"], data.get("timezone", 0))
        sunset = unix_to_time(data["sys"]["sunset"], data.get("timezone", 0))
        icon_code = data["weather"][0]["icon"]

        emoji = WEATHER_EMOJIS.get(weather_main, "")
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_image = Image.open(io.BytesIO(icon_response.content))
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo

        info_text = (
            f"Weather in {city}:\n"
            f"Condition: {weather_desc} {emoji}\n"
            f"Temperature: {temp}°C 🌡️\n"
            f"Humidity: {humidity}% 💧\n"
            f"Wind Speed: {wind_speed} m/s 🌬️\n"
            f"Pressure: {pressure} hPa\n"
            f"Sunrise: {sunrise} 🌅\n"
            f"Sunset: {sunset} 🌇"
        )
        result_label.config(text=info_text)
        save_last_city(city)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Network Error", f"Couldn't retrieve data: {e}")
        result_label.config(text="")
    finally:
        search_button.config(state=NORMAL)


app = Tk()
app.title("CloudPeek Weather App")
app.geometry("400x450")
app.resizable(False, False)
app.configure(bg="#87CEEB")

title_font = ("Helvetica", 18, "bold")
info_font = ("Helvetica", 12)
temp_font = ("Helvetica", 22, "bold")

entry_frame = Frame(app, bg="#87CEEB")
entry_frame.pack(pady=20)

city_entry = Entry(entry_frame, font=("Arial", 16), width=20)
city_entry.pack(side=LEFT, padx=(10, 5))
city_entry.focus_set()

search_button = Button(entry_frame, text="Get Weather", font=(
    "Arial", 12, "bold"), bg="#0052cc", fg="white", command=get_weather)
search_button.pack(side=LEFT)

icon_label = Label(app, bg="#87CEEB")
icon_label.pack()

result_label = Label(app, text="", font=info_font,
                     bg="#87CEEB", justify=LEFT, wraplength=380)
result_label.pack(pady=20)

last_city = load_last_city()
if last_city:
    city_entry.insert(0, last_city)
    get_weather()

app.mainloop()
