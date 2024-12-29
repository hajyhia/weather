import streamlit as st
from weather import weather_tools as wt
import datetime
import matplotlib.pyplot as plt
import math
import os


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

        weather_location_time = wt.get_weather_location_time(weather_data["coord"])
        if local_timezone:
            formatted_time_display = weather_location_time["local"]["time"]
        else:
            formatted_time_display = weather_location_time["current"]["time"]

        beaufort_scale = wt.calculate_beaufort_scale(wind_speed)
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


def display_weather_hourly_forecast(df):
    now_ = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
    df = df[df['dt'].apply(lambda dt_: datetime.datetime.fromtimestamp(dt_)) >= now_].head(10)

    # format hourly label
    df['hourly'] = df['dt'].apply(lambda dt_: datetime.datetime.fromtimestamp(dt_).strftime("%I %p"))

    # Example data
    x = df['hourly']
    y = df['temp']

    # Create a line plot
    plt.figure(figsize=(8, 4))
    # plt.plot(x, y, color = 'red')
    plt.plot(x, y, marker='o', linestyle='-', color='orange', label='Line Plot')

    # Add labels to each point
    for i, label in enumerate(y):
        plt.text(x[i], y[i], f"{label}°", fontsize=10, ha='left', va='bottom')

    plt.xticks(rotation=90)

    labels = list(range(math.floor(min(y)), math.ceil(max(y) + 1), 1))
    plt.yticks(ticks=labels, labels=[f"{s}°" for s in labels])

    # Customize the chart
    plt.title('Hourly forecast', fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.4, axis="y")
    plt.ylabel('Temperature', fontsize=12)
    plt.legend()

    # Show the plot
    with st.container(border=True):
        st.pyplot(plt)


def main():
    st.title("Welcome to the Weather App")

    with st.form("my_form"):
        # Add input widgets to the form
        city_name = st.text_input("Enter the name of the city:")
        local_timezone = st.checkbox("Display date and time in the local timezone")
        store_hourly_forecast = st.checkbox("Store Hourly forecast")

        # Add a submit button
        submitted = st.form_submit_button("Submit")

    if submitted:
        # Display a personalized message
        if city_name:
            weather_data = wt.fetch_weather(city_name)
            display_weather(weather_data, local_timezone)

            # render plot chart for hourly forecast
            hourly_weather_df = wt.pull_weather_hourly_forecast(weather_data)
            display_weather_hourly_forecast(hourly_weather_df)
            if store_hourly_forecast:
                hourly_weather_df.to_csv("hourly_weather_data.csv")
                if os.path.exists("hourly_weather_data.csv"):
                    st.success("The Hourly Forecast is stored in hourly_weather_data.csv successfully.")
        else:
            st.warning("Please enter city name to see the message!")


if __name__ == "__main__":
    main()
