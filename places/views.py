import json
import urllib

from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from places.models import Image, Location

from where_to_go.settings import BASE_DIR


def location(request, id):
    location = get_object_or_404(Location, id=id)
    if location:
        images = Image.objects.filter(location__title=location.title)
        image_links = [link.image.url for link in images]
    geo_json = {
        "title": f"{location.title}",
        "places_id": f"{location.id}",
        "imgs": image_links,
        "description_short": f"{location.short_description}",
        "description_long": f"{location.long_description}",
        "coordinates": {
            "lat": f"{location.long}",
            "lng": f"{location.lat}",
        }
    }
    return JsonResponse(
        geo_json,
        json_dumps_params={
            'indent': 2,
            'ensure_ascii': False
            }
            )


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
                  "placeId": f"{place.id}",
                  "detailsUrl": f"{url}"
                }
              },
            ]
        }

        locations.append(location)
    places_geojson = {"locations": locations}

    return render(request, 'index.html', context=places_geojson)


def get_json(request, json_file):
    filepath = f"{BASE_DIR}/places/geo_json/{json_file}"
    filepath = urllib.parse.unquote(filepath)

    with open(filepath, 'r') as geojson_file:
        geo_json = json.load(geojson_file)
    return JsonResponse(
        geo_json,
        safe=False,
        json_dumps_params={
            'ensure_ascii': False
            }
        )
