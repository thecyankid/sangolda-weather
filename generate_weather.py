import json
import html
import urllib.request
from datetime import datetime, timezone

# Sangolda, Goa
LAT = 15.53085
LON = 73.82465

API = (
    "https://api.open-meteo.com/v1/forecast?"
    f"latitude={LAT}&longitude={LON}"
    "&current=temperature_2m,relative_humidity_2m,"
    "apparent_temperature,precipitation,weather_code,"
    "wind_speed_10m"
    "&daily=weather_code,temperature_2m_max,temperature_2m_min,"
    "precipitation_probability_max,precipitation_sum,"
    "sunrise,sunset"
    "&timezone=Asia%2FKolkata"
    "&forecast_days=7"
)


def weather_description(code):
    codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Freezing drizzle",
        57: "Heavy freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Heavy rain showers",
        85: "Snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }

    return codes.get(code, "Unknown")


def weather_emoji(code):
    if code == 0:
        return "☀️"
    elif code in (1, 2):
        return "🌤️"
    elif code == 3:
        return "☁️"
    elif code in (45, 48):
        return "🌫️"
    elif code in (51, 53, 55, 56, 57,
                  61, 63, 65, 66, 67):
        return "🌧️"
    elif code in (80, 81, 82):
        return "🌦️"
    elif code in (95, 96, 99):
        return "⛈️"
    else:
        return "🌥️"


# ---------------------------------------------------------
# Download weather data
# ---------------------------------------------------------

with urllib.request.urlopen(API) as response:
    data = json.load(response)


current = data["current"]
daily = data["daily"]


# ---------------------------------------------------------
# Current date/time
# ---------------------------------------------------------

updated = datetime.now().strftime("%d %B %Y, %I:%M %p")

today_date = datetime.fromisoformat(
    daily["time"][0]
)

today_name = today_date.strftime("%A")
today_date_formatted = today_date.strftime("%d %B %Y")


# ---------------------------------------------------------
# Current weather
# ---------------------------------------------------------

current_code = current["weather_code"]
current_description = weather_description(current_code)
current_icon = weather_emoji(current_code)


# ---------------------------------------------------------
# Build HTML content
# ---------------------------------------------------------

content = f"""
<html>
<head>
<meta charset="UTF-8">

<title>Sangolda Weather</title>

<style>

body {{
    font-family: sans-serif;
    font-size: 1.1em;
    line-height: 1.5;
}}

h1 {{
    text-align: center;
}}

h2 {{
    margin-top: 25px;
}}

hr {{
    margin: 20px 0;
}}

.current-temperature {{
    font-size: 1.6em;
    font-weight: bold;
}}

.forecast {{
    margin-bottom: 12px;
}}

</style>

</head>

<body>

<h1>SANGOLDA WEATHER</h1>

<p style="text-align:center;">
<b>{today_name}, {today_date_formatted}</b>
</p>

<hr>

<h2>{current_icon} CURRENT</h2>

<p>

<span class="current-temperature">
🌡️ {current["temperature_2m"]}°C
</span>

<br>

Feels like {current["apparent_temperature"]}°C

<br>

{current_icon} {current_description}

<br>

💧 Humidity {current["relative_humidity_2m"]}%

<br>

💨 Wind {current["wind_speed_10m"]} km/h

</p>

<hr>

<h2>TODAY</h2>

<p>

<b>
{daily["temperature_2m_max"][0]}°
/
{daily["temperature_2m_min"][0]}°
</b>

<br>

🌧️ Rain: {daily["precipitation_probability_max"][0]}%

</p>

<hr>

<h2>NEXT 5 DAYS</h2>

"""


# ---------------------------------------------------------
# 5-day forecast
# ---------------------------------------------------------

for i in range(1, 6):

    date = datetime.fromisoformat(
        daily["time"][i]
    )

    day_name = date.strftime("%a")

    high = daily["temperature_2m_max"][i]
    low = daily["temperature_2m_min"][i]

    rain_probability = daily[
        "precipitation_probability_max"
    ][i]

    code = daily["weather_code"][i]

    icon = weather_emoji(code)

    description = weather_description(code)

    content += f"""
<div class="forecast">

<b>{day_name}</b>
&nbsp;&nbsp;
{high}°/{low}°
&nbsp;&nbsp;
{icon}

<br>

<small>
{description} · Rain {rain_probability}%
</small>

</div>
"""


# ---------------------------------------------------------
# Sunrise / sunset
# ---------------------------------------------------------

sunrise = daily["sunrise"][0][11:16]
sunset = daily["sunset"][0][11:16]


content += f"""

<hr>

<h2>SUN</h2>

<p>

🌅 Sunrise: {sunrise}

<br>

🌇 Sunset: {sunset}

</p>

<hr>

<p>

<small>

Updated: {updated}

<br><br>

Weather data provided by Open-Meteo.

</small>

</p>

</body>
</html>
"""


# ---------------------------------------------------------
# RSS feed
# ---------------------------------------------------------

title = "Sangolda Weather"

description = (
    "Current weather and 5-day forecast "
    "for Sangolda, Goa."
)


# Escape RSS metadata
rss_title = html.escape(title)
rss_description = html.escape(description)


# ---------------------------------------------------------
# Generate RSS XML
#
# IMPORTANT:
# The <link> inside <item> is required by KOReader's
# RSS parser.
# ---------------------------------------------------------

now = datetime.now(timezone.utc)

pub_date = now.strftime(
    "%a, %d %b %Y %H:%M:%S GMT"
)


rss = f'''<?xml version="1.0" encoding="UTF-8"?>

<rss version="2.0"
xmlns:content="http://purl.org/rss/1.0/modules/content/">

<channel>

<title>{rss_title}</title>

<link>https://open-meteo.com/</link>

<description>{rss_description}</description>

<language>en</language>

<item>

<title>{rss_title}</title>

<link>https://open-meteo.com/</link>

<description>{rss_description}</description>

<content:encoded>

<![CDATA[

{content}

]]>

</content:encoded>

<pubDate>{pub_date}</pubDate>

<guid isPermaLink="false">Sangolda-Weather</guid>

</item>

</channel>

</rss>
'''


# ---------------------------------------------------------
# Save RSS file
# ---------------------------------------------------------

with open(
    "weather.xml",
    "w",
    encoding="utf-8"
) as f:

    f.write(rss)


print("Sangolda weather RSS generated successfully.")
