import streamlit as st
from weather import weather_api
# import requests
# import datetime
# import pytz
# from timezonefinder import TimezoneFinder

# # Constants
# API_KEY = st.secrets["general"]["api_key"]
# BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
# BEAUFORT_SCALE_URL = "https://openweathermap.org/themes/openweathermap/assets/vendor/mosaic/data/wind-speed-new-data.json"
#
#
# def fetch_weather(city_name):
#     params = {
#         "q": city_name,
#         "appid": API_KEY,
#         "units": "metric"  # Use "imperial" for Fahrenheit
#     }
#
#     try:
#         response = requests.get(BASE_URL, params=params)
#         response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching weather data: {e}")
#         return None
#
#
# def calculate_beaufort_scale(wind_speed):
#     try:
#         response = requests.get(BEAUFORT_SCALE_URL)
#         response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
#         if response.ok and response.json():
#             beaufort_scale_json = response.json().get("en")
#             for scale_name, scale_data in beaufort_scale_json.items():
#                 if scale_data["speed_interval"][0] < wind_speed < scale_data["speed_interval"][1]:
#                     return scale_name
#
#         return None
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching weather data: {e}")
#         return None
#
#
# def get_weather_location_time(weather_data_coordinators):
#     if weather_data_coordinators:
#         local_time = datetime.datetime.now()
#         formatted_local_time = local_time.strftime("%A, %d %B %Y at %I:%M %p")
#
#         # Find timezone
#         tf = TimezoneFinder()
#         timezone = tf.timezone_at(lat=weather_data_coordinators["lat"], lng=weather_data_coordinators["lon"])
#
#         # Get the current time in the timezone
#         tz = pytz.timezone(timezone)
#         current_time = datetime.datetime.now(tz)
#         formatted_current_time = current_time.strftime("%b %d, %I:%M %p")
#         # formatted_current_time = current_time.strftime("%A, %d %B %Y at %I:%M %p")
#         # formatted_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
#
#         return {
#             "local": {"time": formatted_local_time, "timezone": None},
#             "current": {"time": formatted_current_time, "timezone": timezone}
#         }
#
#     else:
#         print("Unable to display weather data.")


def display_weather(weather_data, local_timezone):
    if weather_data:
        city = weather_data["name"]
        country = weather_data["sys"]["country"]
        temp = weather_data["main"]["temp"]
        feels_like = weather_data["main"]["feels_like"]
        weather = weather_data["weather"][0]["description"]
        weather_icon = weather_data["weather"][0]["icon"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]

        weather_location_time = weather_api.get_weather_location_time(weather_data["dt"], weather_data["coord"])
        if local_timezone:
            formatted_time_display = weather_location_time["local"]["time"]
        else:
            formatted_time_display = weather_location_time["current"]["time"]

        beaufort_scale = weather_api.calculate_beaufort_scale(wind_speed)
        with st.container(border=True):
            st.html(f"""
                <div">
                    <div>
                        <span style="color: #de1b2d">{formatted_time_display}</span>
                        <h2 style="margin-top: 0px;">{city}, {country}</h2>
                    </div>
                    <div>
                        <div style="display:flex; flex-direction:row; white-space:nowrap">
                            <img src="http://openweathermap.org/img/wn/{weather_icon}@2x.png" width="50px" >
                            <span style="font-size:36px; font-weight:00; margin-right:8pt">{temp}°C</span>
                        </div>
                        <div style="font-weight:600">Feels like {feels_like}°C. {weather.capitalize()}. {beaufort_scale}</div> 
                    </div>
                </div>
            """)
    else:
        st.write("Unable to display weather data.")


def main():
    st.title("Welcome to the Weather App")

    with st.form("my_form"):
        # st.header("Form Input Section")

        # Add input widgets to the form
        city_name = st.text_input("Enter the name of the city:")
        local_timezone = st.checkbox("Display time by local timezone")

        # Add a submit button
        submitted = st.form_submit_button("Submit")

    if submitted:
        # Display a personalized message
        if city_name:
            weather_data = weather_api.fetch_weather(city_name)
            display_weather(weather_data, local_timezone)
        else:
            st.warning("Please enter city name to see the message!")


if __name__ == "__main__":
    main()
