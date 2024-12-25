import streamlit as st
from weather import weather_api


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

        weather_location_time = weather_api.get_weather_location_time(weather_data["coord"])
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
