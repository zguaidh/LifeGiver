from flask import Flask, request, jsonify
import requests



# Replace 'YOUR_API_KEY' with your actual Google Maps API key
GOOGLE_MAPS_API_KEY = 'AIzaSyAckhaG8lpWrO3lI8shmnOBrTQzeQCV-ew'

def geocode_address(address):
    response = requests.get(
        'https://maps.googleapis.com/maps/api/geocode/json',
        params={'address': address, 'key': GOOGLE_MAPS_API_KEY}
    )
    data = response.json()
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    return None, None


def calculate_distance(address1, address2):


    lat1, lng1 = geocode_address(address1)
    lat2, lng2 = geocode_address(address2)
    if None in [lat1, lng1, lat2, lng2]:
        print({'error': 'Unable to geocode one or both addresses'})

    response = requests.get(
        'https://maps.googleapis.com/maps/api/distancematrix/json',
        params={
            'origins': f'{lat1},{lng1}',
            'destinations': f'{lat2},{lng2}',
            'key': GOOGLE_MAPS_API_KEY
        }
    )
    data = response.json()
    if data['status'] == 'OK':
        distance = data['rows'][0]['elements'][0]['distance']['text']
        return jsonify({'distance': distance})
    print({'error': 'Error calculating distance'})


distance = calculate_distance('Rabat', 'CasaBlanca')
print(distance)