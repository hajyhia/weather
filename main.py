import streamlit as st
import requests
import datetime
import pytz
from timezonefinder import TimezoneFinder

# Constants
API_KEY = st.secrets["general"]["api_key"]
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


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


def dispaly_weather_location_time(weather_data_coordinators):
    if weather_data_coordinators:
        local_time = datetime.datetime.now()
        formatted_local_time = local_time.strftime("%Y-%m-%d %H:%M:%S")

        # Find timezone
        tf = TimezoneFinder()
        timezone = tf.timezone_at(lat=weather_data_coordinators["lat"], lng=weather_data_coordinators["lon"])

        # Get the current time in the timezone
        tz = pytz.timezone(timezone)
        current_time = datetime.datetime.now(tz)
        formatted_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        st.subheader(f"Your local date and time: {formatted_local_time}")
        st.subheader(f"Date and time in '{timezone}': {formatted_current_time}")

    else:
        print("Unable to display weather data.")


def display_weather(weather_data):
    if weather_data:
        city = weather_data["name"]
        temp = weather_data["main"]["temp"]
        weather = weather_data["weather"][0]["description"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]

        with st.container():
            st.header(f"Weather in {city}")
            st.text(f"""
                Temperature: {temp}°C
                Condition: {weather.capitalize()}
                Humidity: {humidity}%
                Wind Speed: {wind_speed} m/s
            """)

    else:
        st.write("Unable to display weather data.")


def main():
    # Set the title of the app
    st.title("Welcome to the Weather App")

    # Get user input for name
    city_name = st.text_input("Enter the name of the city:", placeholder="Enter city name here").strip()

    # Add a button
    if st.button("Submit"):
        # Display a personalized message
        if city_name:
            weather_data = fetch_weather(city_name)
            display_weather(weather_data)
            dispaly_weather_location_time(weather_data["coord"])
        else:
            st.warning("Please enter city name to see the message!")


if __name__ == "__main__":
    main()
