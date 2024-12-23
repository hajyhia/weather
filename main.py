import streamlit as st
import requests

# Constants
API_KEY = st.secrets["general"]["api_key"]
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


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
            # st.success(f"Hello, {name}! You are {age} years old.")
            weather_data = fetch_weather(city_name)
            display_weather(weather_data)
        else:
            st.warning("Please enter city name to see the message!")


if __name__ == "__main__":
    main()
