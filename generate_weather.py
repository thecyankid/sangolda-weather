import json
import html
import urllib.request
from datetime import datetime

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
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Heavy rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with heavy hail",
    }
    return codes.get(code, "Unknown")

with urllib.request.urlopen(API) as response:
    data = json.load(response)

current = data["current"]
daily = data["daily"]

updated = datetime.now().strftime("%d %B %Y, %I:%M %p")

content = f"""
<html>
<head>
<meta charset="UTF-8">
<title>Sangolda Weather</title>
</head>
<body>

<h1>Sangolda Weather</h1>

<p><b>Updated:</b> {updated}</p>

<hr>

<h2>Current Conditions</h2>

<p><b>Temperature:</b> {current["temperature_2m"]}°C</p>
<p><b>Feels like:</b> {current["apparent_temperature"]}°C</p>
<p><b>Conditions:</b> {weather_description(current["weather_code"])}</p>
<p><b>Humidity:</b> {current["relative_humidity_2m"]}%</p>
<p><b>Wind:</b> {current["wind_speed_10m"]} km/h</p>
<p><b>Precipitation:</b> {current["precipitation"]} mm</p>

<hr>

<h2>7-Day Forecast</h2>
"""

for i in range(7):
    date = datetime.fromisoformat(daily["time"][i]).strftime("%A, %d %B")

    content += f"""
<h3>{date}</h3>
<p>
<b>{weather_description(daily["weather_code"][i])}</b><br>
High: {daily["temperature_2m_max"][i]}°C<br>
Low: {daily["temperature_2m_min"][i]}°C<br>
Rain probability: {daily["precipitation_probability_max"][i]}%<br>
Rain: {daily["precipitation_sum"][i]} mm<br>
Sunrise: {daily["sunrise"][i][11:16]}<br>
Sunset: {daily["sunset"][i][11:16]}
</p>
"""

content += """
<hr>
<p><small>
Weather data provided by Open-Meteo.
</small></p>

</body>
</html>
"""

title = "Sangolda Weather"
description = "Current conditions and 7-day forecast for Sangolda, Goa."

rss = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
xmlns:content="http://purl.org/rss/1.0/modules/content/">

<channel>

<title>{html.escape(title)}</title>

<link>https://open-meteo.com/</link>

<description>{html.escape(description)}</description>

<item>

<title>{html.escape(title)}</title>

<description>{html.escape(description)}</description>

<content:encoded>
<![CDATA[
{content}
]]>
</content:encoded>

<pubDate>{datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")}</pubDate>

<guid>Sangolda-Weather</guid>

</item>

</channel>
</rss>
'''

with open("weather.xml", "w", encoding="utf-8") as f:
    f.write(rss)

print("Weather RSS generated successfully.")
