                                                                                <b>Daily Weather Monitoring system</b>
                                                            
                                                        
##Project OverView:

Daily Weather Monitoring system is a python program that automatically collects weather information from the weather.com site every 15 minutes and records it. It tracks daily temperature changes and stores this data in a database. At the end of each day, it also calculates and saves the day's lowest, highest, and average temperatures. This system helps in keeping a consistent check on weather conditions.

###Installation and setup:

1. Initially wrote the python code in the Google colab
   https://colab.research.google.com/drive/1RxGw_YBFnAYcMMLA2Y5wBbKP2AEp2uyy#scrollTo=CSMfeb2P7kOs
3. Created the file in the repository in Github Weather.py and pulled the file using
   preet@dbs-class:~/AI$ cd
   preet@dbs-class:~$ cd AI
   preet@dbs-class:~/AI$ git pull origin main
4. Installed the required packages
   pip install beautifulsoup4
   pip install pymssql
5. https://github.com/20025478/AI/blob/main/Weather.py  ->script to be pulled

###Tools Used:

-Python
-GitHub
-SQL Database

###Website Used:
https://weather.com/en-IE/weather/today/l/EIXX0014:1:EI?Goto=Redirected

##Data Acquisition:

###Sources:

For collecting weather data, the project utilizes web scraping to directly perform database extraction.

###Tools:

The script uses the Python 'requests' library to fetch pages from the weather.com site and the BeautifulSoup library to parse HTML content, extracting relevant weather details.

###Tasks:

The script is designed to reliably access and retrieve weather data from a website. It includes error handling mechanisms to manage potential issues like HTTP errors, ensuring smooth operation during data collection.
<sub>scrape_weather()</sub> function collects weather data from weather.com using 'requests' and extracts details with BeautifulSoup, managing errors like HTTP problems for reliability.


##Data Preprocessing:

###Feature Extraction:

The script identifies and extracts key weather-related data such as temperature, location, and weather conditions from HTML content using BeautifulSoup.

###Data Cleaning:

In the project, the script checks if the weather website has the information it needs. If some info isn't there, the script writes "NA" instead. This way, all the data stays neat and usable for the next steps.

###Data Transformation:

The script converts extracted temperature data into float types for numerical analysis and aggregates daily temperature data for summary statistics.

###Tools:

The script mainly uses BeautifulSoup for HTML parsing and basic Python functions for data handling,as the data processing needs are currently straightforward.
<sub>extract_weather_details()</sub> function searches through the webpage to gather key weather data information like location and temperature,weather updates and then ensures that, it's complete and ready for analysis.



##Data Storage :

###Database System:

The script utilizes a Microsoft SQL Server for storing the scraped weather data and then calculates the min and max temp of the day and then finds the avarage of the temperature.

###Tools:

The pymssql library is used to establish connections and interact with the SQL Server database from Python.

###Implementation Details:

Functions like save_to_sql and save_summary_to_sql in the code handle the insertion of weather details and daily temperature summaries into the database. These functions create SQL queries to move data around efficiently, making sure it's well-organized and easy to find later on.
<sub>save_to_sql</sub> and <sub>save_summary_to_sql</sub> functions manages the insertion of weather details and daily temperature summaries into the database, respectively.



##Automation:

The script uses the <sub>schedule</sub> library to automatically run the scraping function every 15 minutes and summarize daily weather data at 21:00.


##Error Handling:

The script is designed to handle errors carefully when getting data and working with the database. If something unexpected happens, it keeps track of what went wrong, helping to understand and fix the problem later.


##Caching:

The script saves temporary temperature readings to avoid losing data between sessions.
<sub>load_cache()</sub> and <sub>save_cache()</sub> functions, which respectively load cached data from a JSON file and save new temperature readings to it. Which employs a caching mechanism to save temporary temperature readings, preventing data loss between sessions. 
