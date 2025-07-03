from adminsortable2.admin import SortableAdminMixin
from adminsortable2.admin import SortableStackedInline

from django.contrib import admin
from django.utils.html import format_html

from places.models import Image, Location


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    autocomplete_fields = ['location']


class Imageinline(SortableStackedInline):
    model = Image
    extra = 1
    readonly_fields = [
        "preview",
        ]

    def preview(self, obj):
        return format_html(
            '<img src="{url}" style="max-width:{max_width}px; max-height:{max_height}px;" />',
            url=obj.image.url,
            max_width=200,
            max_height=200,
        )

    fields = ('image', 'preview', 'order')


@admin.register(Location)
class LocationAdmin(SortableAdminMixin, admin.ModelAdmin):
    search_fields = ['title']
    inlines = [
        Imageinline,
        ]
