import requests
import json
import os
from urllib.parse import urlparse
from django.core.management.base import BaseCommand
from places.models import Location, Image
from PIL import Image as PILImage
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.db import IntegrityError
from where_to_go.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Upload data to the database from the command line'

    def get_or_create_locations(self, geo_json):
        location, created = Location.objects.get_or_create(
            title=geo_json["title"],
            description_short=geo_json["description_short"],
            description_long=geo_json["description_long"],
            long=geo_json["coordinates"]["lng"],
            lat=geo_json["coordinates"]["lat"],
            )
        images=geo_json["imgs"]
        
        for order, image_link in enumerate(images, start=1):
            response = requests.get(image_link)
            image = ContentFile(response.content)
    
            image_link = urlparse(image_link)
            path_from_link = image_link.path
            image_name = os.path.basename(path_from_link)

        image_for_location, created = Image.objects.get_or_create(
            order=order,
            location=location,
            )

        image_for_location.image.save(
            f"{image_name}",
            ImageFile(image), 
            save=True,
            )


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
            try:
                print('Creating locations. Please wait...')
                filepath = os.path.join(BASE_DIR, 'places/geo_json')
                for filename in os.listdir(filepath):
                    with open (os.path.join(filepath, filename), 'r') as geo_json:
                        geo_json = json.load(geo_json)
                        self.get_or_create_locations(geo_json)
                print("Locations successfully created!")
            except IntegrityError as error:
                print('ERROR:', error)
            

        if options['url']:
            try:
                print('Location is loading...')
                url = options['url']
                response = requests.get(url)
                geo_json = response.json()
                self.get_or_create_locations(geo_json)
                print('Success!')
                        
            except IntegrityError as error:
                print('ERROR:', error)


 



