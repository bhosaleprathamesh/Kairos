import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Kairos", layout="wide")

# Keys for APIs
KEY = '52bccd15ca404e47859161719251301'
API_KEY = "37f8285f2d0a78bb1807e1ee2faacae4"

# Functions to fetch data
def get_current_data(city):
    url = f'http://api.weatherapi.com/v1/current.json?key={KEY}&q={city}&aqi=yes'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_astronomy_data(city):
    url = f"http://api.weatherapi.com/v1/astronomy.json?key={KEY}&q={city}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_forecast_data(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={KEY}&q={city}&days=5"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Title
st.title('Weather App')
st.subheader('Get real-time weather updates for your city!')

# Input city
city = st.text_input('Enter a city name:')


if city:
    with st.spinner("Fetching all weather data..."):
        current_weather = get_current_data(city)
        astronomy_data = get_astronomy_data(city)
        forecast_data = get_forecast_data(city)
    current_weather = get_current_data(city)
    astronomy_data = get_astronomy_data(city)
    forecast_data = get_forecast_data(city)

    if current_weather and astronomy_data and forecast_data:
        # Create Tabs
        tabs = st.tabs(["🌍 Current Weather", "🌬️ Air Quality", "🌙 Astronomy", "📅 Forecast"])

        # Tab 1: Current Weather
        with tabs[0]:
            st.markdown(f"<h4>City: {current_weather['location']['name']}</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4>Region:{current_weather['location']['region']}</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4>Country:{current_weather['location']['country']}</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4>Last Updated: {current_weather['current']['last_updated']}</h4>", unsafe_allow_html=True)
            st.divider()
            #st.subheader(f"Current Weather: {current_weather['current']['condition']['text']}")
            #st.subheader(f"Current Weather: {current_weather['current']['condition']['icon']}")
            condition_text = current_weather['current']['condition']['text']
            icon_url = current_weather['current']['condition']['icon']

            # Using markdown with unsafe_allow_html to render HTML
            st.markdown(f"<h3>Current Weather: {condition_text} <img src='{icon_url}' width='50' style='vertical-align: middle;'/></h3>", unsafe_allow_html=True)
            
            #COLUMNS
            a,b,c = st.columns(3)
            d,e,f = st.columns(3)
            g,h,i = st.columns(3)
                #temp
            with a:
                a.metric(label="Temperature", value=f"{current_weather['current']['temp_c']} °C🌡️", border=True)
            with b:
                b.metric(label="Feels Like", value=f"{current_weather['current']['feelslike_c']} °C🌡", border=True)

                
                #cloud
            cloud_cover = current_weather['current']['cloud']
            if cloud_cover == 0:
                cloud_description = "Clear sky"
            elif cloud_cover <= 25:
                cloud_description = "Mostly clear"
            elif cloud_cover <= 50:
                cloud_description = "Partly cloudy"
            elif cloud_cover <= 75:
                cloud_description = "Mostly cloudy"
            else:
                cloud_description = "Overcast skies"
            with c:
                c.metric(label="Cloud🌥️", value=f"{cloud_cover}% {cloud_description}", border=True)

                #pressure
            with d:
                d.metric(label="Pressure", value=f"{current_weather['current']['pressure_mb']} mb⏲️", border=True)

                #precipitation
            with e:
                e.metric(label="Precipitation", value=f"{current_weather['current']['precip_mm']} mm🌧️", border=True)


            
                #wind
            with f:
                f.metric(label="Wind Speed", value=f"{current_weather['current']['wind_kph']} km/h💨", border=True)
            with g:
                g.metric(label="Wind Direction", value=f"{current_weather['current']['wind_dir']}🍃 ", border=True)

                #humidity
            with h:
                h.metric(label="Humidity", value=f"{current_weather['current']['humidity']} %💧", border=True)
                
                #UV index
            uv_value = current_weather['current']['uv']
            if uv_value <= 2:
                uv_description = "Low risk"
            elif uv_value <= 5:
                uv_description = "Moderate risk"
            elif uv_value <= 7:
                uv_description =  "High risk"
            elif uv_value <= 10:
                uv_description = "Very high risk"
            else:
                uv_description = "Extreme risk, Avoid going outdoors. Stay indoors or seek complete shade."
            i.metric(label="UV Index", value=f"{uv_value} {uv_description}☀️", border=True)

        # Tab 2: Air Quality
        with tabs[1]:
            #st.subheader('Air Quality Data')
            air_quality = current_weather.get('current', {}).get('air_quality', {})
            if air_quality:
                        aqi = air_quality.get('us-epa-index')
                        if aqi == 1:
                            aqi_desc = 'Good🟢'
                            color= 'green'
                        elif aqi == 2:
                            aqi_desc = "Moderate🔔"
                            color = 'yellow'
                        elif aqi == 3:
                            aqi_desc = 'Unhealthy for senitive group⚠️'
                            color = 'orange'
                        elif aqi == 4:
                            aqi_desc = 'Unhealthy🔴'
                            color = 'red'
                        elif aqi == 5:
                            aqi_desc = 'Very Unhealthy🚨'
                            color = 'red'
                        elif aqi == 6:
                            aqi_desc = 'Hazardous☣️'
                            color = 'red'
                        else:
                            aqi_desc = 'Unknown'
                        #st.metric(label=f"Air Quality Index (AQI)", value=aqi_desc )
                        st.markdown(f"<h3>Air Quality Index (AQI):<span style='color:{color};'> {aqi_desc}</span></h3>", unsafe_allow_html=True)
                        #st.write(f"**GDI**: {air_quality.get('gb-defra-index', 'N/A')}")
                        #st.write(f"**PM2.5**: {air_quality.get('pm2_5', 'N/A')} µg/m³")
                        #st.write(f"**PM10**: {air_quality.get('pm10', 'N/A')} µg/m³")
                        #st.write(f"**CO (Carbon Monoxide)**: {air_quality.get('co', 'N/A')} µg/m³")
                        #st.write(f"**NO2 (Nitrogen Dioxide)**: {air_quality.get('no2', 'N/A')} µg/m³")
                        #st.write(f"**O3 (Ozone)**: {air_quality.get('o3', 'N/A')} µg/m³")
                        #st.write(f"**SO2 (Sulfur Dioxide)**: {air_quality.get('so2', 'N/A')} µg/m³")

                        import streamlit as st

                        # Example air quality data
                        air_quality = {
                            "PM2.5": air_quality.get("pm2_5", "N/A"),
                            "PM10": air_quality.get("pm10", "N/A"),
                            "CO (Carbon Monoxide)": air_quality.get("co", "N/A"),
                            "NO2 (Nitrogen Dioxide)": air_quality.get("no2", "N/A"),
                            "O3 (Ozone)": air_quality.get("o3", "N/A"),
                            "SO2 (Sulfur Dioxide)": air_quality.get("so2", "N/A"),
                        }

                        # Convert dictionary to DataFrame
                        import pandas as pd
                        df = pd.DataFrame.from_dict(air_quality, orient="index", columns=["Concentration (µg/m³)"]).reset_index()
                        df.columns = ["Gases", "Concentration (µg/m³)"]

                        # Display the dataframe
                        st.dataframe(df, use_container_width=False)



            else:
                    st.write("Air quality data is not available.")

        # Tab 3: Astronomy
        with tabs[2]:
            #st.subheader('Solar and Lunar Data 🌙☀️')

            if astronomy_data:
                astro = astronomy_data["astronomy"]["astro"]
                col1, col2 = st.columns(2)

                with col1:
                    st.metric(" Sunrise🌅", f"{astro['sunrise']}")
                    st.metric(" Sunset🌇", f"{astro['sunset']}")

                with col2:
                    st.metric("🌕 Moonrise", astro['moonrise'])
                    st.metric("🌒 Moonset", astro['moonset'])
                if astro:
                    moon = astro['moon_phase']
                    if moon == 'New Moon':
                        moon_desc = 'New Moon🌑'
                    elif moon == 'Waxing Crescent':
                        moon_desc = 'Waxing Crescent🌒'
                    elif moon == 'First Quarter':
                        moon_desc = 'First Quarter🌓'
                    elif moon == 'Waxing Gibbous':
                        moon_desc = 'Waxing Gibbous🌔'
                    elif moon == 'Full Moon':
                        moon_desc = 'Full Moon🌕'
                    elif moon == 'Waning Gibbous':
                        moon_desc = 'Waning Gibbous🌖'
                    elif moon == 'Last Quarter':
                        moon_desc = 'Last Quarter🌗'
                    elif moon == 'Waning Crescent':
                        moon_desc = 'Waning Crescent🌘'
                    else:
                        moon_desc = 'Unknown'
                
                #st.markdown(f"<h4>Air Quality Index (AQI):</h4><h5 style='color:{color};'> {aqi_desc}</h5>", unsafe_allow_html=True)
                st.markdown(f"<h3>Moon Phase:{moon_desc}</h3>", unsafe_allow_html=True)
                moon_illumination = int(astro['moon_illumination'])
                st.write(f"**Moon Illumination**: {moon_illumination}%")
                st.progress(moon_illumination / 100)
            else:
                st.error("Could not fetch astronomy data. Please check the city name.")
        # Tab 4: Forecast
        with tabs[3]:
            url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
            response = requests.get(url)
            data = response.json()

            import re

            # Grouped patterns with icons
            weather_patterns = {
                r'thunderstorm': '🌩️',  # Matches "thunderstorm"
                r'rain|drizzle': '🌧️',  # Matches "rain" or "drizzle"
                r'snow': '☃️',          # Matches "snow"
                r'clear': '🌞',         # Matches "clear sky"
                r'clouds': '☁️',        # Matches "clouds"
                r'mist|fog': '🌫️',      # Matches "mist" or "fog"
                r'haze': '🌁',
                r'sand':'🏜️',
                r'volcanic ash':'🌋',
                r'tornado|squalls|sand whirls|dust whirls':'🌪️'
            }

            # Fallback icon for unmatched descriptions
            default_icon = '☁️'

            forecast_data = []

            for entry in data['list']:
                date_time = entry['dt_txt']
                description = entry['weather'][0]['description']
                
                # Format date and time
                formatted_date_time = pd.to_datetime(date_time).strftime('%d %b %I %p')
                
                # Find the first matching condition
                icon = default_icon
                first_match_start = float('inf')  # Track the position of the first match
                for pattern, pattern_icon in weather_patterns.items():
                    match = re.search(pattern, description, re.IGNORECASE)  # Case-insensitive matching
                    if match:
                        # Check if this match appears earlier than previous matches
                        if match.start() < first_match_start:
                            first_match_start = match.start()
                            icon = pattern_icon
                
                # Add data to the list
                forecast_data.append([formatted_date_time, description, icon])

            # Create a DataFrame
            df = pd.DataFrame(forecast_data, columns=["Date & Time", "Weather Description", "Icon"])

            # Combine the weather description and icon into one column for display
            df['Weather Info'] = df.apply(lambda row: f"{row['Weather Description']} {row['Icon']}", axis=1)

            # Remove original "Weather Description" and "Icon" columns to keep the table clean
            df_display = df.drop(columns=['Weather Description', 'Icon'])

            # Display the DataFrame with only the combined "Weather Info" column
            st.subheader('5-Day Weather Forecast')
            st.dataframe(df_display)

    else:
        st.error("Could not fetch weather data. Please check the city name.")
else:
    st.warning("Please enter a city name to see weather updates.")

#st.markdown(
    #'Powered by <a href="https://www.weatherapi.com/" title="Free Weather API" target="_blank">WeatherAPI.com</a>',
    #unsafe_allow_html=True
#)
st.markdown(
    """
    <footer style="padding: 10px; margin-top: 50px;">
        <p>Powered by <a href="https://www.weatherapi.com/" target="_blank">WeatherAPI.com</a></p>
        <p>Developed by <a href="https://github.com/bhosaleprathamesh" target="_blank">PB36</a></p>
    </footer>
    """,
    unsafe_allow_html=True
)

