#!/usr/bin/python
# OpenWeather using Python

"""
Usage: Python-OpenWeather.py

Makes API calls to OpenWeather and retrievs JSON data
Parses JSON data using JSON library

List of city ID in JSON format can be obtained from
http://bulk.openweathermap.org/sample/

Options
_______

-h or help  Displays this message
"""

import urllib
import json
import codecs
import gzip
from sys import argv, exit

if len(argv) > 1:
    print(__doc__)
    exit(0)



def city():
    city = raw_input('Enter city name: ')
    city = city.lower()
    print "Retrieving weather information for %s ....." % city
    
    return city

def citysearch(city):
    listCities = []
    with codecs.open('city.list.json', 'r', encoding='utf8') as cityList:
        for cl in cityList:
            cityJSON = json.loads(cl)
            cityName = cityJSON['name']
            cityName = cityName.lower()
            if cityName == city:
                searchCity = cityJSON
                listCities.append(searchCity)
    
    cityList.close()

    print "Your search resulted in", len(listCities), "cities with the name %s" % city

    if len(listCities) > 1:
	print "Please refine your search and choose the ID relevant to the country"
        for listCity in listCities:
	    print "Country: %s, " % listCity['country'], "ID: %s" % listCity['_id']
	cityID = raw_input("Enter the relevant ID: ")
	print "You have entered %s" % cityID
   
    elif len(listCities) == 1:
        cityID = listCities[0]['_id']
        print "Country:", listCities[0]['country']

    elif len(listCities) == 0:
        print "Your city does not exist"
        exit(0)

    return cityID 		

city = city()
locationID = citysearch(city)

apikey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
serviceUrl = "http://api.openweathermap.org/data/2.5/weather?"
url = serviceUrl + urllib.urlencode({'id': locationID, 'APPID': apikey})
urlRead = urllib.urlopen(url).read()
dataJSON = json.loads(urlRead)

temp = float(dataJSON['main']['temp']) - 273.0
tempMax = float(dataJSON['main']['temp_max']) - 273.0
tempMin = float(dataJSON['main']['temp_min']) - 273.0
humidity = int(dataJSON['main']['humidity'])
wind = dataJSON['wind']
windSpeed = float(dataJSON['wind']['speed'])
condition = dataJSON['weather'][0]['description']

print ""
print "*******************"
print "--Weather Summary--"
print "*******************"
print "Current Temperature: %.2f C" % temp
print "Maximum Temperature: %.2f C" % tempMax
print "Minimum Temperature: %.2f C" % tempMin
print "Humidity: %d %%" % humidity

if 'gust' in wind:
    windGust = float(dataJSON['wind']['gust'])
    print "Wind Gust:%s km/hr" % windGust
else:
    print "Wind Gust: Data not available"

print "Wind Speed: %.2f km/hr" % windSpeed
print "Condition: %s" % condition

