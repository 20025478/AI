import requests
from bs4 import BeautifulSoup
import schedule
import time
import os
import pandas as pd
import pymssql

# Global list to store temperature readings
temperature_readings = []

def scrape_weather():
    url = 'https://weather.com/en-IE/weather/today/l/EIXX0014:1:EI?Goto=Redirected'
    html = requests.get(url)
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'html.parser')
    else:
        print(f"Error fetching data, status code: {html.status_code}")
        return

    weather_details = {'Location':'NA', 'Timestamp': 'NA', 'Weather Update': 'NA', 'Temperature': 'NA', 'Day night temp': 'NA', 'Alert': 'NA', 'Climate Now': 'NA', 'Climate Info': 'NA'}

    location_tag = soup.find('h1', class_='CurrentConditions--location--1YWj_')
    timestamp_tag = soup.find('span', class_='CurrentConditions--timestamp--1ybTk')
    weather_update_tag = soup.find('div', class_='CurrentConditions--phraseValue--mZC_p')
    temperature_tag = soup.find('span', class_='CurrentConditions--tempValue--MHmYY')
    day_night_temp_tag = soup.find('div', class_='CurrentConditions--tempHiLoValue--3T1DG')
    alert_headline_tag = soup.find('h2', class_='AlertHeadline--alertText--38xov')
    climate_now_tag = soup.find("h2", class_='InsightNotification--headline--3gJfC PrecipIntensityCard--InsightHeadline--22w7Q')
    climate_info_tag = soup.find("p", class_='InsightNotification--text--35QdL')

    weather_details['Location'] = location_tag.text.strip() if location_tag else 'NA'
    weather_details['Timestamp'] = timestamp_tag.text.strip().replace('As of','') if timestamp_tag else 'NA'
    weather_details['Weather Update'] = weather_update_tag.text.strip() if weather_update_tag else 'NA'
    weather_details['Temperature'] = temperature_tag.text.strip() if temperature_tag else 'NA'
    weather_details['Day night temp'] = day_night_temp_tag.text.strip().replace('•', '/') if day_night_temp_tag else 'NA'
    weather_details['Alert'] = alert_headline_tag.text.strip() if alert_headline_tag else 'NA'
    weather_details['Climate Now'] = climate_now_tag.text.strip() if climate_now_tag else 'NA'
    weather_details['Climate Info'] = climate_info_tag.text.strip() if climate_info_tag else 'NA'

    if temperature_tag:
        temp_value = temperature_tag.text.strip()[:-1]
        if temp_value.replace('.', '', 1).isdigit():
            temperature_readings.append(float(temp_value))

    print_console(weather_details)
    save_to_excel(weather_details)
    sql_connection(weather_details)

def print_console(weather_details):
    for key, value in weather_details.items():
        print(f"{key}: {value}")

def save_to_excel(weather_details):
    convert_data_df = pd.DataFrame([weather_details])
    excel_file_path = 'weather_data.xlsx'
    try:
        if os.path.exists(excel_file_path):
            existing_data_df = pd.read_excel(excel_file_path, index_col=None)
            updated_data_df = pd.concat([existing_data_df, convert_data_df], ignore_index=True)
        else:
            updated_data_df = convert_data_df
        updated_data_df.to_excel(excel_file_path, index=False)
        print("Data saved successfully in excel format")
    except Exception as e:
        print(f"Error: {e}")

def sql_connection(weather_details):
    server = '20025478.database.windows.net'
    user = 'preethi'
    password = 'Lokesh98@'
    database = '20025478_2024-04-09T15-08Z'
    conn = None
    try:
        conn = pymssql.connect(server, user, password, database)
        cursor = conn.cursor()
        sql = """INSERT INTO Weather_data_info (Location, Timestamp, Weather_Update, Temperature, Day_Night_Temp, Alert, Climate_Now, Climate_Info)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (weather_details['Location'], weather_details['Timestamp'], weather_details['Weather Update'],
                             weather_details['Temperature'], weather_details['Day night temp'], weather_details['Alert'],
                             weather_details['Climate Now'], weather_details['Climate Info']))
        conn.commit()
        print("Weather data saved to SQL database successfully")
    except Exception as e:
        print(f"SQL Connection Error: {e}")
    finally:
        if conn is not None:
            conn.close()

def summarize_day():
    if temperature_readings:
        min_temp = min(temperature_readings)
        max_temp = max(temperature_readings)
        average_temp = sum(temperature_readings) / len(temperature_readings)
        print(f"Daily Min Temp: {min_temp}, Max Temp: {max_temp}, Avg Temp: {average_temp}")
        sql_connection_summary(min_temp, max_temp, average_temp)

def sql_connection_summary(min_temp, max_temp, average_temp):
    server = '20025478.database.windows.net'
    user = 'preethi'
    password = 'Lokesh98@'
    database = '20025478_2024-04-09T15-08Z'
    conn = None
    try:
        conn = pymssql.connect(server, user, password, database)
        cursor = conn.cursor()
        sql = """INSERT INTO Daily_Summary (Min_Temp, Max_Temp, Average_Temp)
                 VALUES (%s, %s, %s)"""
        cursor.execute(sql, (min_temp, max_temp, average_temp))
        conn.commit()
        print("Daily summary saved to SQL database successfully")
    except Exception as e:
        print(f"SQL Connection Error: {e}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    schedule.every(60).seconds.do(scrape_weather)
    schedule.every(60).seconds.do(summarize_day)
    #schedule.every().day.at("21:00").do(summarize_day)
    while True:
        schedule.run_pending()
        time.sleep(1)
