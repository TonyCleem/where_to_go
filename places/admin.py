from django.contrib import admin
from places.models import *

# Register your models here.


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


class Imageinline(admin.TabularInline):
    model = Image


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = [
        Imageinline,
        ]

