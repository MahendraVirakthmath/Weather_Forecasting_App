import requests
import tkinter as tk
import re
from decouple import config
from PIL import Image, ImageTk

OPEN_WEATHER_MAP_API_KEY = config("OPEN_WEATHER_MAP_API_KEY", default="default-weather-api-key")
OPEN_WEATHER_MAP_API_ENDPOINT = 'https://api.openweathermap.org/data/2.5/weather'

IPBASE_API_KEY = config("IPBASE_API_KEY", default="default-ipbase-api-key")
IPBASE_API_ENDPOINT = "https://api.ipbase.com/v2/info"

IP_ADDRESS_REGEX = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def get_weather():
    input_value = input_field.get()

    if IP_ADDRESS_REGEX.match(input_value):
        ipbase_query_params = {
            "apiKey": IPBASE_API_KEY,
            "ip": input_value
        }
        response = requests.get(IPBASE_API_ENDPOINT,
                                params=ipbase_query_params)
        city_name = response.json()["data"]["location"]["city"]["name"]

        weather_query_params = {
            'q': city_name,
            'appid': OPEN_WEATHER_MAP_API_KEY,
            'units': 'metric'
        }
        response = requests.get(
            OPEN_WEATHER_MAP_API_ENDPOINT, params=weather_query_params)
        weather_data = response.json()

    else:
        # Try to get weather data directly using city name
        weather_query_params = {
            'q': input_value,
            'appid': OPEN_WEATHER_MAP_API_KEY,
            'units': 'metric'
        }
        response = requests.get(
            OPEN_WEATHER_MAP_API_ENDPOINT, params=weather_query_params)
        weather_data = response.json()

    # Display weather data
    weather_label.config(
        text=f"{weather_data['name']}: {weather_data['main']['temp']}°C")


def get_location_weather():
    query_params = {
        "apiKey": IPBASE_API_KEY
    }
    response = requests.get(IPBASE_API_ENDPOINT, params=query_params)
    city_name = response.json()["data"]["location"]["city"]["name"]

    weather_query_params = {
        'q': city_name,
        'appid': OPEN_WEATHER_MAP_API_KEY,
        'units': 'metric'
    }
    response = requests.get(
        OPEN_WEATHER_MAP_API_ENDPOINT, params=weather_query_params)
    weather_data = response.json()

    # Display weather data
    weather_label.config(
        text=f"{weather_data['name']}: {weather_data['main']['temp']}°C")


root = tk.Tk()
root.title("Weather Forecasting App")
root.geometry("400x300")

title_label = tk.Label(root, text="Weather Forecasting App", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

input_label = tk.Label(root, text="Enter city or IP address:")
input_label.pack()

input_field = tk.Entry(root)
input_field.pack()

submit_button = tk.Button(root, text="Get Weather", command=get_weather, width=20)
submit_button.pack(pady=5)

location_button = tk.Button(root, text="Use Current Location", command=get_location_weather, width=20)
location_button.pack(pady=5)


weather_icon = Image.open('./cloudy.png')
weather_icon = weather_icon.resize((64, 64))
weather_icon = ImageTk.PhotoImage(weather_icon)

weather_label = tk.Label(root, text="", font=("Arial", 12), wraplength=380)
weather_label.pack(pady=10)

root.iconphoto(True, weather_icon)


root.mainloop()