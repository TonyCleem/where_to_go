import json
import urllib

from django.conf import settings
from django.db.models import Prefetch
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from places.models import Image, Location


BASE_DIR = settings.BASE_DIR


def location(request, id):
    location = get_object_or_404(
        Location.objects.prefetch_related(
            Prefetch(
                'images',
                queryset=Image.objects.all(),
                to_attr='all_images',
            )
        ),
        pk=id
    )
    image_links = [link.image.url for link in location.all_images]
    geo_json = {
        "title": location.title,
        "places_id": location.id,
        "imgs": image_links,
        "description_short": location.short_description,
        "description_long": location.long_description,
        "coordinates": {
            "lat": location.long,
            "lng": location.lat,
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
    locations = {
            "type": "FeatureCollection",
            "features": []
        }
    for place in places:
        url = reverse('location', args=[place.id])
        location = {
            "type": "Feature",
            "geometry": {
              "type": "Point",
              "coordinates": [place.long, place.lat]
            },
            "properties": {
              "title": place.title,
              "placeId": place.id,
              "detailsUrl": url,
            },
        }
        locations['features'].append(location)
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
