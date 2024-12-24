import requests
import datetime
import pytz
from timezonefinder import TimezoneFinder

# Constants
API_KEY = "a97bfd1e514bbcb662cacbee64cb8eab"  # Replace with your OpenWeatherMap API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
BEAUFORT_SCALE_URL = "https://openweathermap.org/themes/openweathermap/assets/vendor/mosaic/data/wind-speed-new-data.json"


def fetch_weather(city_name):
    """
    Fetches weather data for the given city.

    Args:
        city_name (str): Name of the city.

    Returns:
        dict: Weather information if successful, None otherwise.
    """
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


def fetch_beaufort_scale():
    try:
        response = requests.get(BEAUFORT_SCALE_URL)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


def dispaly_weather_location_time(weather_data_coordinators):
    if weather_data_coordinators:
        local_time = datetime.datetime.now()
        formatted_date = local_time.strftime("%Y-%m-%d %H:%M:%S")  # Example: '2024-12-23 14:30:45'
        print(f"Your local date and time:: {formatted_date}")

        # Find timezone
        tf = TimezoneFinder()
        timezone = tf.timezone_at(lat=weather_data_coordinators["lat"], lng=weather_data_coordinators["lon"])

        # Get the current time in the timezone
        tz = pytz.timezone(timezone)
        current_time = datetime.datetime.now(tz)
        formatted_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"Date and time in {timezone}: {formatted_current_time}")
    else:
        print("Unable to display weather data.")


def display_weather(weather_data):
    """
    Displays weather information in a user-friendly format.

    Args:
        weather_data (dict): Weather data from the API.
    """
    if weather_data:
        city = weather_data["name"]
        temp = weather_data["main"]["temp"]
        weather = weather_data["weather"][0]["description"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]

        print(f"\nWeather in {city}:")
        print(f"Temperature: {temp}°C")
        print(f"Condition: {weather.capitalize()}")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")
    else:
        print("Unable to display weather data.")


def main():
    """
    Main function to run the weather app.
    """
    print("Welcome to the Weather App!")
    city_name = input("Enter the name of the city: ").strip()
    weather_data = fetch_weather(city_name)
    display_weather(weather_data)
    dispaly_weather_location_time(weather_data["coord"])


if __name__ == "__main__":
    main()
