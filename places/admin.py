from django.contrib import admin
from places.models import *
from django.utils.html import format_html

# Register your models here.


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


class Imageinline(admin.TabularInline):
    model = Image
    readonly_fields = [
        "get_preview",
        ]

    def get_preview(self, obj):
        return format_html('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image.url,
            width=200,
            height=200,
            )
    )

    fields = ('image', 'get_preview', 'order')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = [
        Imageinline,
        ]
