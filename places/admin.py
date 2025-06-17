from django.contrib import admin
from places.models import *
from django.utils.html import format_html
from adminsortable2.admin import SortableStackedInline
from adminsortable2.admin import SortableAdminMixin


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


class Imageinline(SortableStackedInline):
    model = Image
    extra = 1
    readonly_fields = [
        "preview",
        ]

    def preview(self, obj):
        return format_html('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image.url,
            width=200,
            height=200,
            )
    )

    fields = ('image', 'preview', 'order')


@admin.register(Location)
class LocationAdmin(SortableAdminMixin, admin.ModelAdmin):
    search_fields =  ['title']
    inlines = [
        Imageinline,
        ]