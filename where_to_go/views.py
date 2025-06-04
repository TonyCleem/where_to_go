from django.http import HttpResponse
from django.shortcuts import render
from places.models import Location, Image

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

