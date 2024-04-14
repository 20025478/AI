                                                                                        
**Course:** B9AI108 PROGRAMMING FOR DATA ANALYSIS (B9AI108_2324_TMD2)

**Lecturer:** paul-laird

**Student Name:** Preethi Manoharan

**Student ID:** 20025478

                                                            
## Project Title: Daily weather Monitoring                                                       
### Project Overview:
Daily Weather Monitoring system is a python program that automatically collects weather information from the weather.com site every 15 minutes and records it. It tracks daily temperature changes and stores this data in a database. At the end of each day, it also calculates and saves the day's lowest, highest, and average temperatures. This system helps in keeping a consistent check on weather conditions.

### Installation and setup:
1. <b>Development:</b> The initial Python code was developed in Google Colab. The working notebook is available at:
   https://colab.research.google.com/drive/1RxGw_YBFnAYcMMLA2Y5wBbKP2AEp2uyy#scrollTo=CSMfeb2P7kOs
2. <b>Version Control:</b> The code was then moved to GitHub for version control and collaboration. The main script can be found at:
   https://github.com/20025478/AI/blob/main/Weather.py
3. <b>Environment Setup:</b> The script was pulled into a Microsoft Azure Virtual Machine environment using the command:
   <sub>git pull origin main</sub>
4. <b>Dependency Installation:</b> Necessary Python packages were installed via pip in theMicrosoft Azure Virtual Machine environment using the command:
   pip install beautifulsoup4
   pip install pymssql
5. <b>Running the Script:</b> To ensure the script runs continuously, even after closing the terminal, the following command was used:
  <sub>nohup python3 Weather.py &</sub>  ,This command runs the script in the background and outputs the log to nohup.out

### Tools Used:
-Python

-GitHub

-SQL Database

### Website Used:
https://weather.com/en-IE/weather/today/l/EIXX0014:1:EI?Goto=Redirected

## Data Acquisition:
### Sources:
For collecting weather data, the project utilizes web scraping to directly perform database extraction.
### Tools:
The script uses the Python 'requests' library to fetch the page from the weather.com site and the BeautifulSoup library to parse HTML content, extracting relevant weather details.
### Tasks:
<sub>scrape_weather()</sub> function collects weather data from weather.com using 'requests' and extracts details with BeautifulSoup, managing errors like HTTP problems for reliability.


## Data Preprocessing:
### Feature Extraction:
<sub>extract_weather_details()</sub> function ,identifies and extracts key weather-related data such as temperature, location, and weather conditions from HTML content using BeautifulSoup.
### Data Cleaning:
In cases where the data is not available, your script assigns 'NA' to maintain consistency in your dataset. This is evident in your conditional checks within the <sub>extract_weather_details()</sub>  function.
### Data Transformation:
The script converts extracted temperature data into float types for numerical analysis and aggregates daily temperature data for summary statistics.
### Data Aggregation: 
<sub>summarize_day()</sub> function, Summarize the detailed data into more useful forms, such as calculating minimum, maximum, and average values of the day.
### Data Loading: 
<sub>save_to_sql()</sub> function, loads the processed data into a SQL database, effectively storing the transformed and aggregated data for further use.
### Tools:
The script mainly uses BeautifulSoup for HTML parsing and basic Python functions for data handling,as the data processing needs are currently straightforward.
<sub>extract_weather_details()</sub> function searches through the webpage to gather key weather data information like location and temperature,weather updates and then ensures that, it's complete and ready for analysis.


## Data Storage :
### Database System:
Microsoft SQL Server is utilized for persistent storage of weather data.
### Tools:
The pymssql library is used to establish connections and interact with the SQL Server database from Python.
### Implementation Details:
Weather details and temperature summaries are efficiently inserted into the database by <sub>save_to_sql()</sub> and <sub>save_summary_to_sql()</sub> functions and making sure it's well-organized and easy to find later on.


## Automation:
The script uses the <sub>schedule</sub> library to automatically run the scraping function every 15 minutes and summarize daily weather data at 21:00.

## Error Handling:
The script is designed to handle errors carefully when getting data and working with the database. If something unexpected happens, it keeps track of what went wrong, helping to understand and fix the problem later.

## Caching:
The script saves temporary temperature readings to avoid losing data between sessions.
<sub>load_cache()</sub> and <sub>save_cache()</sub> functions, which respectively load cached data from a JSON file and save new temperature readings to it. Which employs a caching mechanism to save temporary temperature readings, preventing data loss between sessions. 
