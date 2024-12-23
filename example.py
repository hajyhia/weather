import requests

# Constants
API_KEY = "a97bfd1e514bbcb662cacbee64cb8eab"  # Replace with your OpenWeatherMap API key
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

if __name__ == "__main__":
    main()
