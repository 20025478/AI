import requests
from bs4 import BeautifulSoup
import schedule
import time
import pymssql

temperature_readings = []

def scrape_weather():
    url = 'https://weather.com/en-IE/weather/today/l/EIXX0014:1:EI?Goto=Redirected'
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        weather_details = extract_weather_details(soup)

        if weather_details['Current Temperature'] != 'NA':
            temp_value = weather_details['Current Temperature'].replace('°', '')
            if temp_value.replace('.', '', 1).isdigit():
                temperature_readings.append(float(temp_value))

        save_to_sql(weather_details)
        print_console(weather_details)

    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as e:
        print(f"An error occurred: {e}")

def extract_weather_details(soup):
    try:
        location_tag = soup.find('h1', class_='CurrentConditions--location--1YWj_')
        timestamp_tag = soup.find('span', class_='CurrentConditions--timestamp--1ybTk')
        temperature_tag = soup.find('span', class_='CurrentConditions--tempValue--MHmYY')
        day_night_temp_tag = soup.find('div', class_='CurrentConditions--tempHiLoValue--3T1DG')
        weather_update_tag = soup.find('div', class_='CurrentConditions--phraseValue--mZC_p')
        alert_headline_tag = soup.find('h2', class_='AlertHeadline--alertText--38xov')
        climate_now_tag = soup.find("h2", class_='InsightNotification--headline--3gJfC PrecipIntensityCard--InsightHeadline--22w7Q')
        climate_info_tag = soup.find('div', class_='CurrentConditions--precipValue--RBVJT')

        weather_details = {
            'Location': location_tag.get_text(strip=True) if location_tag else 'NA',
            'Timestamp': timestamp_tag.get_text(strip=True).replace('As of', '') if timestamp_tag else 'NA',
            'Current Temperature': temperature_tag.get_text(strip=True) if temperature_tag else 'NA',
            'Day Temp': '',
            'Night Temp': '',
            'Weather Update':weather_update_tag.get_text(strip=True) if weather_update_tag else 'NA',
            'Alert': alert_headline_tag.get_text(strip=True) if alert_headline_tag else 'NA',
            'Climate Now': climate_now_tag.get_text(strip=True) if climate_now_tag else 'NA',
            'Climate Info': climate_info_tag.get_text(strip=True) if climate_info_tag else 'NA',
        }

        if day_night_temp_tag:
            temperature_tags = day_night_temp_tag.find_all('span', {'data-testid': 'TemperatureValue'})
            if temperature_tags and len(temperature_tags) >= 2:
                weather_details['Day Temp'] = temperature_tags[0].get_text(strip=True)
                weather_details['Night Temp'] = temperature_tags[1].get_text(strip=True)
        return weather_details
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def print_console(weather_details):
    for key, value in weather_details.items():
        print(f"{key}: {value}")

def save_to_sql(weather_details):
    server = '20025478.database.windows.net'
    user = 'preethi'
    password = 'Lokesh98@'
    database = '20025478_2024-04-09T15-08Z'

    day_night_temp = f"{weather_details['Day Temp']} / {weather_details['Night Temp']}"

    conn = None
    try:
        conn = pymssql.connect(server, user, password, database)
        cursor = conn.cursor()
        sql = """
            INSERT INTO Weather_data_info (
                Location, Timestamp, Weather_Update, Current_Temperature,
                Day_temp, Night_temp, Alert, Climate_Now, Climate_Info
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            weather_details['Location'], weather_details['Timestamp'], weather_details['Weather Update'],
            weather_details['Current Temperature'], weather_details['Day Temp'], weather_details['Night Temp'],
            weather_details['Alert'], weather_details['Climate Now'], weather_details['Climate Info'],
        ))
        conn.commit()
        print("Weather data saved to SQL database successfully")
    except Exception as e:
        print(f"SQL Connection Error: {e}")
    finally:
        if conn:
            conn.close()

def summarize_day():
    if not temperature_readings:
        print("No temperature data to summarize.")
        return

    min_temp = min(temperature_readings)
    max_temp = max(temperature_readings)
    average_temp = sum(temperature_readings) / len(temperature_readings)
    print(f"Daily Min Temp: {min_temp}, Max Temp: {max_temp}, Avg Temp: {average_temp}")

    temperature_readings.clear()
    save_summary_to_sql(min_temp, max_temp, average_temp)

def save_summary_to_sql(min_temp, max_temp, average_temp):
    server = '20025478.database.windows.net'
    user = 'preethi'
    password = 'Lokesh98@'
    database = '20025478_2024-04-09T15-08Z'

    conn = None
    try:
        conn = pymssql.connect(server, user, password, database)
        cursor = conn.cursor()
        sql = "INSERT INTO Daily_Summary (Min_Temp, Max_Temp, Average_Temp) VALUES (%s, %s, %s)"
        cursor.execute(sql, (min_temp, max_temp, average_temp))
        conn.commit()
        print("Daily summary saved to SQL database successfully")
    except Exception as e:
        print(f"SQL Connection Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    schedule.every(60).seconds.do(scrape_weather)
    schedule.every().day.at("21:00").do(summarize_day)
    while True:
        schedule.run_pending()
        time.sleep(1)
