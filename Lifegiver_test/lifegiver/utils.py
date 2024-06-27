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


distance = calculate_distance('Rabat, Morocco', 'CasaBlanca, Morocco')
print(distance)


def return_match(blood_type):
    matching_types = []
    if blood_type[1] == '+':
        matching_types.extend(('O-', 'O+'))
        if blood_type[0] != 'O':
            matching_types.extend((blood_type[0]+'-', blood_type))
    
    elif blood_type[1] == '-':
        matching_types.extend(('O-'))
        if blood_type[0] != 'O':
            matching_types.extend((blood_type))
        
    elif blood_type[2] == '-':
        matching_types.extend(('O-', 'A-', 'B-', 'AB-'))

    else:
        matching_types.extend(('O-', 'A-', 'B-', 'AB-', 'O+', 'A+', 'B+', 'AB+'))
        
    return matching_types

blood_type = 'O+'
print(return_match(blood_type))