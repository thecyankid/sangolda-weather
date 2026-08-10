import json
import html
import urllib.request
from datetime import datetime, timezone

# =========================================================
# SANGOLDA, GOA
# =========================================================

LAT = 15.53085
LON = 73.82465


# =========================================================
# OPEN-METEO API
# =========================================================

API = (
    "https://api.open-meteo.com/v1/forecast?"
    f"latitude={LAT}&longitude={LON}"
    "&current="
    "temperature_2m,"
    "relative_humidity_2m,"
    "apparent_temperature,"
    "precipitation,"
    "weather_code,"
    "wind_speed_10m"
    "&daily="
    "weather_code,"
    "temperature_2m_max,"
    "temperature_2m_min,"
    "precipitation_probability_max,"
    "precipitation_sum,"
    "sunrise,"
    "sunset"
    "&timezone=Asia%2FKolkata"
    "&forecast_days=7"
)


# =========================================================
# WEATHER CODE → TEXT
# =========================================================

def weather_description(code):

    codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",

        45: "Fog",
        48: "Fog",

        51: "Light drizzle",
        53: "Drizzle",
        55: "Heavy drizzle",

        56: "Freezing drizzle",
        57: "Heavy freezing drizzle",

        61: "Light rain",
        63: "Moderate rain",
        65: "Heavy rain",

        66: "Freezing rain",
        67: "Heavy freezing rain",

        71: "Light snow",
        73: "Moderate snow",
        75: "Heavy snow",

        77: "Snow grains",

        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Heavy rain showers",

        85: "Snow showers",
        86: "Heavy snow showers",

        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with heavy hail",
    }

    return codes.get(code, "Unknown")


# =========================================================
# DOWNLOAD WEATHER
# =========================================================

with urllib.request.urlopen(API) as response:
    data = json.load(response)


current = data["current"]
daily = data["daily"]


# =========================================================
# DATE
# =========================================================

today = datetime.fromisoformat(
    daily["time"][0]
)

today_name = today.strftime("%A")
today_date = today.strftime("%d %B %Y")

updated = datetime.now().strftime(
    "%d %B %Y, %I:%M %p"
)


# =========================================================
# CURRENT CONDITIONS
# =========================================================

current_condition = weather_description(
    current["weather_code"]
)


# =========================================================
# HTML CONTENT
#
# Deliberately simple HTML because KOReader converts
# this RSS article into EPUB and we want it to look good
# on a 6-inch Kindle screen.
# =========================================================

content = f"""
<html>

<head>

<meta charset="UTF-8">

<title>Sangolda Weather</title>

<style>

body {{
    font-family: serif;
    font-size: 1.05em;
    line-height: 1.45;
    margin: 0;
    padding: 0;
}}

h1 {{
    font-size: 1.5em;
    text-align: center;
    margin-bottom: 0.2em;
}}

.date {{
    text-align: center;
    margin-bottom: 1.2em;
}}

h2 {{
    font-size: 1.2em;
    margin-top: 1.3em;
    margin-bottom: 0.4em;
}}

.section {{
    border-top: 1px solid #888;
    padding-top: 0.7em;
}}

.row {{
    margin: 0.25em 0;
}}

.day {{
    margin-top: 0.8em;
    margin-bottom: 0.1em;
    font-weight: bold;
}}

.details {{
    margin-left: 1em;
}}

.footer {{
    margin-top: 1.5em;
    font-size: 0.8em;
}}

</style>

</head>

<body>


<h1>SANGOLDA WEATHER</h1>

<div class="date">
{today_name}, {today_date}
</div>


<div class="section">

<h2>CURRENT</h2>

<p>

<div class="row">
<b>Temperature:</b>
{current["temperature_2m"]}°C
</div>

<div class="row">
<b>Feels like:</b>
{current["apparent_temperature"]}°C
</div>

<div class="row">
<b>Conditions:</b>
{current_condition}
</div>

<div class="row">
<b>Humidity:</b>
{current["relative_humidity_2m"]}%
</div>

<div class="row">
<b>Wind:</b>
{current["wind_speed_10m"]} km/h
</div>

</p>

</div>


<div class="section">

<h2>TODAY</h2>

<p>

<div class="row">
<b>High:</b>
{daily["temperature_2m_max"][0]}°C
</div>

<div class="row">
<b>Low:</b>
{daily["temperature_2m_min"][0]}°C
</div>

<div class="row">
<b>Rain probability:</b>
{daily["precipitation_probability_max"][0]}%
</div>

<div class="row">
<b>Expected rain:</b>
{daily["precipitation_sum"][0]} mm
</div>

</p>

</div>


<div class="section">

<h2>NEXT 5 DAYS</h2>
"""


# =========================================================
# 5-DAY FORECAST
# =========================================================

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

    rain_amount = daily[
        "precipitation_sum"
    ][i]

    condition = weather_description(
        daily["weather_code"][i]
    )

    content += f"""

<div class="day">

{day_name} &nbsp;&nbsp; {high}° / {low}°C

</div>

<div class="details">

{condition}

<br>

Rain probability: {rain_probability}%

<br>

Expected rain: {rain_amount} mm

</div>

"""


# =========================================================
# SUNRISE / SUNSET
# =========================================================

sunrise = daily["sunrise"][0][11:16]
sunset = daily["sunset"][0][11:16]


content += f"""

</div>


<div class="section">

<h2>SUN</h2>

<p>

<b>Sunrise:</b> {sunrise}

<br>

<b>Sunset:</b> {sunset}

</p>

</div>


<div class="footer">

Updated: {updated}

<br><br>

Weather data provided by Open-Meteo.

</div>


</body>

</html>
"""


# =========================================================
# RSS METADATA
# =========================================================

title = "Sangolda Weather"

description = (
    "Current weather and 5-day forecast "
    "for Sangolda, Goa."
)

rss_title = html.escape(title)
rss_description = html.escape(description)


# =========================================================
# RSS PUBLICATION DATE
# =========================================================

now = datetime.now(timezone.utc)

pub_date = now.strftime(
    "%a, %d %b %Y %H:%M:%S GMT"
)


# =========================================================
# RSS XML
#
# IMPORTANT:
# KOReader requires <link> inside <item>.
# =========================================================

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

<guid isPermaLink="false">
Sangolda-Weather
</guid>

</item>


</channel>

</rss>
'''


# =========================================================
# WRITE RSS FILE
# =========================================================

with open(
    "weather.xml",
    "w",
    encoding="utf-8"
) as f:

    f.write(rss)


print(
    "Sangolda weather RSS generated successfully."
)
