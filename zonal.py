import requests
import datetime
import pytz
from timezonefinder import TimezoneFinder

city = "Paris"
cordi = {"coord": {
    "lon": 2.3488,
    "lat": 48.8534
}}
tf = TimezoneFinder()

# Get the local timezone
local_timezone = datetime.datetime.now(pytz.timezone('local')).tzinfo
print(f"Local timezone: {local_timezone}")

local_time = datetime.datetime.now()
formatted_date = local_time.strftime("%Y-%m-%d %H:%M:%S")  # Example: '2024-12-23 14:30:45'
print(f"Local time: {formatted_date}")

# Find timezone

longitude=lng=cordi["coord"]["lon"]
latitude=cordi["coord"]["lat"]
timezone = tf.timezone_at(lat=cordi["coord"]["lat"], lng=cordi["coord"]["lon"])

# Display timezone and current time
print(f"City: {city}")
print(f"Timezone: {timezone}")

# Get the current time in the timezone
tz = pytz.timezone(timezone)
current_time = datetime.datetime.now(tz)
formated_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
print(f"Current time in {city}: {formated_current_time}")