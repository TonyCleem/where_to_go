from django.db import models
from tinymce.models import HTMLField


class Location(models.Model):
    title = models.CharField(
        max_length=200,
        default='',
        blank=False,
        verbose_name="Название места",
        )

    place_id = models.CharField(
        max_length=200,
        default='',
        blank=False,
    )
    
    description_short = models.TextField(
        default='',
        blank=True,
    )
    description_long = HTMLField(
        default = '',
        blank = True
    )
    
    long = models.FloatField(
        null=True,
        blank=False,
    )
    lat = models.FloatField(
        null=True,
        blank=False,
    )

    class Meta:
        ordering = ['place_id']


    def __str__(self):
        return self.title


class Image(models.Model):
    order = models.IntegerField(
        null=True,
        blank=False,
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to="media/"
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '%s %s' % (self.order, self.location)