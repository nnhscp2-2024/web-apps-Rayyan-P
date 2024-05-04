"""
Name:
Title: Weather App
Description: Make a weather web app using Flask and Openweathermap API
"""
# imports for Flask, API calls, City class
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for  
import requests
from city import City

# list of City objects
cities = []
API_KEY = "dcb9deb505067260a9d290e0f4030b13"

def get_data(city):
	"""
	Returns API data from a given city string.

	Parameters:
	city (str): The name of the city to fetch data for.

	Returns:
	list: A list of data fetched from the API, with the city name as the first element.
	"""

	# list of data fetched from API
	data = [city.title()]
	# insert code to get API data (Step 3)

	# initialize your API key here
	API_KEY = 'dcb9deb505067260a9d290e0f4030b13'

	# request data from API and retrieve json data response
	url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
	response = requests.get(url)

	# convert json response into python dictionary
	response = response.json()
	print(response)

	dict = response.get('main')
	current_temp = dict.get('temp')
	data.append(current_temp)

	# get current description from dictionary and add it to the data list
	current_desc = response.get('weather')[0].get('description')
	data.append(current_desc.title())

	temp_feel = response.get("main").get("feels_like")
	data.append(temp_feel)

	min_temp = response.get("main").get("temp_min")
	data.append(min_temp)

	max_temp = response.get("main").get("temp_max")
	data.append(max_temp)

	windSpeed = response.get("wind").get("speed")
	data.append(windSpeed)

	return data

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
	return render_template('index.html') 

@app.route('/', methods = ['POST'])
def index2():
	# get the city name from the form's search box
	city_str = request.form["search_box"]
	dataOfCity = get_data(city_str)
	print(dataOfCity)

	cityWeather = City(dataOfCity[0], dataOfCity[1], dataOfCity[2], dataOfCity[3], dataOfCity[4], dataOfCity[5], dataOfCity[6])
	cityWeather.get_feel_in_C()
	cityWeather.get_feel_in_F()
	cityWeather.get_max_in_C()
	cityWeather.get_max_in_F()
	cityWeather.get_min_in_C()
	cityWeather.get_min_in_F()
	cityWeather.get_temp_in_C()
	cityWeather.get_temp_in_F()
	cityWeather.get_wind_speed()

	cities.append(cityWeather)

	return render_template('index.html', city = city_str, tempC = cityWeather.tempC, tempF = cityWeather.tempF, minC = cityWeather.minC, minF = cityWeather.minF, maxC = cityWeather.maxC, maxF = cityWeather.maxF, feelC = cityWeather.feelC, feelF = cityWeather.feelF, windSpeed = cityWeather.wind, desc = cityWeather.desc)

app.run(host='0.0.0.0', port=8080) # any code below 'app.run' line won't run