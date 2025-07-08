import json
import os
import sys
import time
from urllib.parse import urlparse

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from places.models import Image, Location

import requests

from where_to_go.settings import BASE_DIR


def error_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_or_create_locations(geo_json):
        location, created = Location.objects.get_or_create(
            title=geo_json["title"],
            defaults={
                'short_description': geo_json["description_short"],
                'long_description': geo_json["description_long"],
                'long': geo_json["coordinates"]["lng"],
                'lat': geo_json["coordinates"]["lat"],
            }
        )
        images = geo_json["imgs"]
        count_connections = 0
        for order, image_link in enumerate(images, start=1):
            while True:
                try:
                    response = requests.get(image_link, timeout=10)
                    response.raise_for_status()
                    image_link = urlparse(image_link)
                    path_from_link = image_link.path
                    image_name = os.path.basename(path_from_link)
                    image_for_location, created = Image.objects.get_or_create(
                        location=location,
                        image=ContentFile(response.content, name=f'{image_name}'),
                        defaults={
                            'order': order,
                        }
                    )
                    if count_connections:
                        print('')
                        print('Connection is established')
                        count_connections = 0
                    break
                except IntegrityError as error:
                    print('ERROR:', error)
                    break
                except requests.exceptions.HTTPError as error:
                    print('HTTPError: Invalid URL')
                    error_print(error)
                    break
                except requests.exceptions.ConnectionError as error:
                    print('ConnectionError: No internet connection\nAttempt to reconnect')
                    time.sleep(10)
                    error_print(error)
                    count_connections += 1


class Command(BaseCommand):
    help = 'Upload data to the database from the command line'

    def add_arguments(self, parser):
        parser.add_argument(
            'url',
            nargs='?',
            type=str,
            help="Uploading by url in the format 'https://address/file.json'",
        )

        parser.add_argument(
            '-a',
            '--all',
            action='store_true',
            help="Upload all location in folder 'places/geo_json'"
        )

    def handle(self, *args, **options):
        if options['all']:
            print('Creating locations. Please wait...')
            filepath = os.path.join(BASE_DIR, 'places/geo_json')
            for filename in os.listdir(filepath):
                with open(os.path.join(filepath, filename), 'r') as geo_json:
                    geo_json = json.load(geo_json)
                    get_or_create_locations(geo_json)
            print("Locations successfully created!")
        if options['url']:
            count_connections = 0
            while True:
                try:
                    print('Location is loading...')
                    url = options['url']
                    response = requests.get(url)
                    response.raise_for_status()
                    geo_json = response.json()
                    get_or_create_locations(geo_json)
                    if count_connections:
                        print('')
                        print('Connection is established')
                        count_connections = 0
                    print('Success!')
                    break
                except IntegrityError as error:
                    print('ERROR:', error)
                    break
                except requests.exceptions.HTTPError as error:
                    print('HTTPError: Invalid URL')
                    error_print(error)
                    break
                except requests.exceptions.ConnectionError as error:
                    print('ConnectionError: No internet connection\nAttempt to reconnect')
                    time.sleep(10)
                    error_print(error)
                    count_connections += 1
