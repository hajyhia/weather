import streamlit as st
import weather_app
import datetime
import pytz
from timezonefinder import TimezoneFinder
import requests

weather_data = weather_app.fetch_weather("London, GB")


if weather_data:
    city = weather_data["name"]
    temp = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]
    weather = weather_data["weather"][0]["description"]
    weather_icon = weather_data["weather"][0]["icon"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]

    with st.container(border=True):
        st.header(f"Weather in {city}")
        st.text(f"""
                Temperature: {temp}°C
                Condition: {weather.capitalize()}
                Humidity: {humidity}%
                Wind Speed: {wind_speed} m/s
            """)
        # st.html('<img src="http://openweathermap.org/img/wn/03d@2x.png" alt="Scattered Clouds">')
        st.image(f"http://openweathermap.org/img/wn/{weather_icon}@2x.png", width=50)

    weather_data_coordinators = weather_data["coord"]
    local_time = datetime.datetime.now()
    formatted_local_time = local_time.strftime("%Y-%m-%d %H:%M:%S")

    # Find timezone
    tf = TimezoneFinder()
    timezone = tf.timezone_at(lat=weather_data_coordinators["lat"], lng=weather_data_coordinators["lon"])

    # Get the current time in the timezone
    tz = pytz.timezone(timezone)
    current_time = datetime.datetime.now(tz)
    formatted_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    # formatted_current_time_ = current_time.strftime("%b %d, %I:%M%p") # Dec 24, 01:15pm
    formatted_current_time_ = current_time.strftime("%A, %d %B %Y at %I:%M %p") # e.g., "Tuesday, 24 December 2024 at 03:30 PM"

    Beaufort_Scale = None
    response = requests.get("https://openweathermap.org/themes/openweathermap/assets/vendor/mosaic/data/wind-speed-new-data.json")
    if response.ok and response.json():
        windSpeedData = response.json().get("en")

        for scale_name, scale_data in windSpeedData.items():
            if scale_data["speed_interval"][0] < wind_speed < scale_data["speed_interval"][1]:
                Beaufort_Scale = scale_name
                break

    st.html(
        f"""
        <div class="current-container mobile-padding">
            <div>
                <span class="orange-text" style="color: #de1b2d">{formatted_current_time_}</span>
                <h2 style="margin-top: 0px;">London, GB</h2>
            </div>
            <div>
                <div class="current-temp" style="display:flex; flex-direction:row; white-space:nowrap">
                    <img src="http://openweathermap.org/img/wn/{weather_icon}@2x.png" width="50px" >
                    <span class="heading" style="font-size:36px; font-weight: 00; margin-right:8pt">{temp}°C</span>
                </div>
                <div class="bold" style="font-weight:600">Feels like {feels_like}°C. {weather.capitalize()}. {Beaufort_Scale} </div>
            </div>
        </div>
        """)

else:
    st.write("Unable to display weather data.")
