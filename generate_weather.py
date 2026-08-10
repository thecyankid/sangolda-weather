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
    "weather_code,"
    "wind_speed_10m"
    "&daily="
    "weather_code,"
    "temperature_2m_max,"
    "temperature_2m_min,"
    "precipitation_probability_max"
    "&timezone=Asia%2FKolkata"
    "&forecast_days=7"
)


# =========================================================
# WEATHER CODE -> TEXT
# =========================================================

def weather_description(code):

    codes = {
        0: "Clear",
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
        81: "Moderate showers",
        82: "Heavy showers",
        85: "Snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm + hail",
        99: "Thunderstorm + heavy hail",
    }

    return codes.get(code, "Unknown")


# =========================================================
# DOWNLOAD WEATHER DATA
# =========================================================

with urllib.request.urlopen(API) as response:
    data = json.load(response)


current = data["current"]
daily = data["daily"]


# =========================================================
# DATE
# =========================================================

today = datetime.fromisoformat(daily["time"][0])

today_name = today.strftime("%A")
today_date = today.strftime("%d %B %Y")

updated = datetime.now().strftime(
    "%d %b %Y, %I:%M %p"
)


# =========================================================
# CURRENT CONDITIONS
# =========================================================

current_condition = weather_description(
    current["weather_code"]
)


# =========================================================
# HTML
#
# Designed specifically for a 6-inch Kindle/PW4.
# Minimal spacing and no emoji.
# =========================================================

content = f"""
<html>

<head>

<meta charset="UTF-8">

<title>Sangolda Weather</title>

<style>

body {{
    font-family: serif;
    font-size: 0.95em;
    line-height: 1.25;
    margin: 0;
    padding: 0;
}}

h1 {{
    font-size: 1.35em;
    text-align: center;
    margin: 0 0 0.15em 0;
}}

.date {{
    text-align: center;
    margin-bottom: 0.55em;
}}

h2 {{
    font-size: 1.05em;
    margin: 0.65em 0 0.25em 0;
    border-bottom: 1px solid #777;
    padding-bottom: 0.15em;
}}

p {{
    margin: 0.2em 0;
}}

.current {{
    text-align: center;
}}

.today {{
    text-align: center;
}}

.forecast {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 0.25em;
    font-size: 0.95em;
}}

.forecast th {{
    border-bottom: 1px solid #777;
    padding: 0.2em;
    text-align: center;
}}

.forecast td {{
    padding: 0.18em 0.2em;
    text-align: center;
}}

.footer {{
    margin-top: 0.65em;
    text-align: center;
    font-size: 0.75em;
}}

</style>

</head>

<body>


<h1>SANGOLDA WEATHER</h1>

<div class="date">
<b>{today_name}, {today_date}</b>
</div>


<h2>CURRENT</h2>

<div class="current">

<p>
<b>{current["temperature_2m"]}°C</b>
&nbsp;&nbsp;|&nbsp;&nbsp;
Feels {current["apparent_temperature"]}°C
</p>

<p>
{current_condition}
&nbsp;&nbsp;|&nbsp;&nbsp;
Humidity {current["relative_humidity_2m"]}%
&nbsp;&nbsp;|&nbsp;&nbsp;
Wind {current["wind_speed_10m"]} km/h
</p>

</div>


<h2>TODAY</h2>

<div class="today">

<p>
<b>
High {daily["temperature_2m_max"][0]}°C
&nbsp;&nbsp;&nbsp;
Low {daily["temperature_2m_min"][0]}°C
</b>
</p>

<p>
Rain probability:
<b>{daily["precipitation_probability_max"][0]}%</b>
</p>

</div>


<h2>NEXT 5 DAYS</h2>

<table class="forecast">

<tr>
<th>DAY</th>
<th>HIGH</th>
<th>LOW</th>
<th>RAIN</th>
</tr>
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

    rain = daily[
        "precipitation_probability_max"
    ][i]

    content += f"""
<tr>

<td><b>{day_name}</b></td>

<td>{high}°</td>

<td>{low}°</td>

<td>{rain}%</td>

</tr>
"""


# =========================================================
# CLOSE TABLE + FOOTER
# =========================================================

content += f"""

</table>


<div class="footer">

Updated {updated}

<br>

Weather: Open-Meteo

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
# RSS DATE
# =========================================================

now = datetime.now(timezone.utc)

pub_date = now.strftime(
    "%a, %d %b %Y %H:%M:%S GMT"
)


# =========================================================
# RSS XML
#
# IMPORTANT:
# The <link> inside <item> is required by KOReader.
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

<guid isPermaLink="false">Sangolda-Weather</guid>

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


print("Sangolda weather RSS generated successfully.")
