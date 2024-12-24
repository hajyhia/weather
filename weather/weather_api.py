import requests
import datetime
import pytz
from timezonefinder import TimezoneFinder
# Constants
# API_KEY = st.secrets["general"]["api_key"]
API_KEY = "a97bfd1e514bbcb662cacbee64cb8eab"
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


def get_weather_location_time(weather_data_time, weather_data_coordinators):
    if weather_data_coordinators:
        local_time = datetime.datetime.fromtimestamp(weather_data_time)
        formatted_local_time = local_time.strftime("%A, %d %B %Y at %I:%M %p")

        # Find timezone
        tf = TimezoneFinder()
        timezone = tf.timezone_at(lat=weather_data_coordinators["lat"], lng=weather_data_coordinators["lon"])

        # Get the current time in the timezone
        tz = pytz.timezone(timezone)
        current_time = datetime.datetime.fromtimestamp(weather_data_time, tz)
        formatted_current_time = current_time.strftime("%b %d, %I:%M %p")
        # formatted_current_time = current_time.strftime("%A, %d %B %Y at %I:%M %p")
        # formatted_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        return {
            "local": {"time": formatted_local_time, "timezone": None},
            "current": {"time": formatted_current_time, "timezone": timezone}
        }

    else:
        print("Unable to display weather data.")