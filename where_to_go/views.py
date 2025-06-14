import json
from django.urls import reverse
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render
from places.models import Location, Image
from django.shortcuts import get_object_or_404


def location(request, place_id):
    location = get_object_or_404(Location, id=place_id)
    if location:
        images = Image.objects.filter(location__title=location.title)
        image_links = [link.image.url for link in images]            

    geo_json = {
        "title": f"{location.title}",
        "imgs": image_links,
        "description_short": f"{location.description_short}",
        "description_long": f"{location.description_long}",
        "coordinates": {
            "lat": f"{location.long}",
            "lng": f"{location.lat}",
        }
    }
    return JsonResponse(geo_json, json_dumps_params={'indent': 2, 'ensure_ascii': False})


def index(request):
    places = Location.objects.all()
    locations = list()
    for place in places:
        url = reverse('location', args=[place.id])

        location = {
            "type": "FeatureCollection",
            "features": [
              {
                "type": "Feature",
                "geometry": {
                  "type": "Point",
                  "coordinates": [place.long, place.lat]
                },
                "properties": {
                  "title": f"{place.title}",
                  "placeId": f"{place.place_id}",
                  "detailsUrl": f"{url}"
                }
              },
            ]
        }

        locations.append(location)     
    places_geojson = {"locations": locations}

    return render(request, 'index.html', context=places_geojson)
