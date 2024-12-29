import requests
import datetime
import pytz
from timezonefinder import TimezoneFinder
import pandas as pd
import streamlit as st

# Constants
API_KEY = st.secrets["general"]["api_key"]
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
BEAUFORT_SCALE_URL = "https://openweathermap.org/themes/openweathermap/assets/vendor/mosaic/data/wind-speed-new-data.json"


def fetch_weather(city_name):
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"  # Use "imperial" for Fahrenheit
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


def calculate_beaufort_scale(wind_speed):
    try:
        response = requests.get(BEAUFORT_SCALE_URL)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        if response.ok and response.json():
            beaufort_scale_json = response.json().get("en")
            for scale_name, scale_data in beaufort_scale_json.items():
                if scale_data["speed_interval"][0] < wind_speed < scale_data["speed_interval"][1]:
                    return scale_name

        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


def get_weather_location_time(weather_data_coordinators):
    if weather_data_coordinators:
        local_time = datetime.datetime.now()
        formatted_local_time = local_time.strftime("%b %d, %I:%M %p")

        # Find timezone
        tf = TimezoneFinder()
        timezone = tf.timezone_at(lat=weather_data_coordinators["lat"], lng=weather_data_coordinators["lon"])

        # Get the current time in the timezone
        tz = pytz.timezone(timezone)
        current_time = datetime.datetime.now(tz)
        formatted_current_time = current_time.strftime("%b %d, %I:%M %p")

        return {
            "local": {"time": formatted_local_time, "timezone": None},
            "current": {"time": formatted_current_time, "timezone": timezone}
        }

    else:
        print("Unable to display weather data.")


# flat the weather_data_ data json to simple array of dics
def reformat_hourly_weather_data(weather_data_):
    new_list = []
    for item in weather_data_["hourly"]:
        new_item = {}
        for key, value in item.items():
            if key != 'weather':
                new_item[key] = value
            else:
                new_item.update(value[0])
        new_list.append(new_item)
    return new_list


def pull_weather_hourly_forecast(weather_data_):
    params = {
        "lat": weather_data_['coord']['lat'],
        "lon": weather_data_['coord']['lon'],
        "appid": "5796abbde9106b7da4febfae8c44c232",
        "units": "metric"
    }

    try:
        response = requests.get("https://api.openweathermap.org/data/2.5/onecall", params=params)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        weather_data = response.json()

        # reformatted weather data json payload
        hourly_weather_data = reformat_hourly_weather_data(weather_data)

        hourly_weather_df = pd.DataFrame(hourly_weather_data)
        return hourly_weather_df
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
