from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, JsonResponse
import csv
import os
import json
import osmnx as ox
import pandas
import requests
import math

def hotelsResponseView(request, cityName):
    
    # city name from path
    city = cityName.upper()
    # prevent to pass favicon.ico or empty string to nominatim request
    if city == '' or city == 'favicon.ico':
        return HttpResponse(status=200)
    # search for hotels only
    tags = {'amenity': 'hotel',
            'building': 'hotel',
            'tourism': 'hotel'}
    # geodataframe with response
    hotelResponse = ox.geometries_from_place(city, tags=tags)
    # dictionary for clean data to return
    hotels = {'hotels': []}
    # iterate over geodataframe and append names to respone dictionary
    # save as much hotels as possible :(
    # bcs for requests are used free tools
    # its necessary to look through all data and recover NaN data if possible 
    for ind in hotelResponse.index:
        hotel = {}
        # check for NaN value
        if hotelResponse['name'][ind] != hotelResponse['name'][ind]:
            # check if geometries are Points
            if hotelResponse['geometry'][ind].geom_type == 'Point':
                # creating string with lat and lng
                place = str(hotelResponse['geometry'][ind].y) + ', ' + str(hotelResponse['geometry'][ind].x)
                # repeat request but now its concentrating to 500m around point(place)
                simpleResp = ox.geometries_from_place(place, tags=tags, buffer_dist=500)
                hotel['name'] = simpleResp['name'][0]
                hotels['hotels'].append(hotel)
            # check if geometries are Polygons
            if hotelResponse['geometry'][ind].geom_type == 'Polygon':
                # repeat request but in specified polygon
                simpleResp = ox.geometries_from_polygon(hotelResponse['geometry'][ind], tags=tags)
                # unfortunetly since simpleResp may not contain hotel name
                # its necessary to look into dataframe and reject data without name column
                if 'name' in simpleResp.columns:
                    hotel['name'] = simpleResp['name'][0]
                    hotels['hotels'].append(hotel)
        # if there is no NaN value then just append it to response dict            
        else:
            hotel['name'] = hotelResponse['name'][ind]
            hotels['hotels'].append(hotel)
    return JsonResponse(hotels)

def cityPageView(request, cityName=''):

    # city name from path
    city = cityName.upper()
    # prevent to pass favicon.ico or empty string to nominatim request
    if city == '' or city == 'favicon.ico':
        return HttpResponse(status=200)
    # search for hotels only
    tags = {'amenity': 'hotel',
            'building': 'hotel',
            'tourism': 'hotel'}
    # geodataframe with response
    hotelResponse = ox.geometries_from_place(city, tags=tags)
    # dictionary for clean data to return
    hotels = {'hotels': []}
    # iterate over geodataframe and append names to respone dictionary
    for ind in hotelResponse.index:
        hotel = {}
        hotel['name'] = hotelResponse['name'][ind]
        hotels['hotels'].append(hotel)
    # response as json
    return JsonResponse(hotels)


def cityQueryView(request, cityName=''):
    cityName = cityName.upper()
    # nasza baza 40k miast
    worldCities = os.path.join(settings.DATA_DIR, 'worldcities.csv')
    # sciezka (upper liwiduje mniejsze wieksze znaki)
    # lista na miasta
    cities = {'metainf': [], 'data': []}
    # znajduje miasta ktore sa na jakas litere
    # jak to dziala to nie czas na tlumaczenie
    if cityName == '':
        return HttpResponse(status=200)
    else:
        count = 0
        with open(worldCities, encoding='utf8') as data:
            for row in data:
                if (((row.split(',')[0])[1:-1]).upper()).startswith(cityName):
                    city = {}
                    city['name'] = (row.split(',')[0])[1:-1]
                    city['lat'] = (row.split(',')[2])[1:-1]
                    city['lng'] = (row.split(',')[3])[1:-1]
                    city['country'] = (row.split(',')[4])[1:-1]
                    city['iso'] = (row.split(',')[6])[1:-1]
                    cities['data'].append(city)
                    count = count + 1
        inf = {}
        inf['count'] = count
        cities['metainf'].append(inf)
        if(inf['count'] == 0):
            return JsonResponse({'message': 'Szukane miasto nie istnieje.'}, status=404)

        return JsonResponse(cities)
