import json
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render
from places.models import Location, Image
from django.shortcuts import get_object_or_404

def index(request):
    places = Location.objects.all() 
    locations = {
        "type": "FeatureCollection",
        "features": [
            {
            "type": "Feature",
            "geometry": {
              "type": "Point",
              "coordinates": [places[0].long, places[0].lat]
              },
            "properties": {
              "title": f"{places[0].title}",
              "placeId": "moscow_legends",
              "detailsUrl": "simple_plug"
              },
            },
            {
            "type": "Feature",
            "geometry": {
              "type": "Point",
              "coordinates": [places[1].long, places[1].lat]
              },
            "properties": {
              "title": f"{places[1].title}",
              "placeId": "roofs24",
              "detailsUrl": "simple_plug"
              },
            },
        ]
    }

    places_geojson = {"locations": locations}

    return render(request, 'index.html', context=places_geojson)


def location(request, place):
    location = get_object_or_404(Location, id=place)
    images = Image.objects.get(id=place).image.url

    geo_json = {
        "title:": f"{location.title}",
        "images": [f"{images}"],
        "description_short": f"{location.description_short}",
        "description_long": f"{location.description_long}",
        "coordinates": {
            "lat": f"{location.long}",
            "lng": f"{location.lat}",
        }
    }
    return JsonResponse(geo_json, json_dumps_params={'indent': 2, 'ensure_ascii': False})
