from django.db import models
from tinymce.models import HTMLField


class Location(models.Model):
    title = models.CharField(
        max_length=200,
        default='',
        blank=False,
        verbose_name="Название места",
        unique=True,
        )

    place_id = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        unique=True,
    )

    description_short = models.TextField(
        default='',
        blank=False,
    )
    description_long = HTMLField(
        default = '',
        blank = False
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
        default=1,
        blank=False,
    )
    image = models.ImageField(
        null=True,
        blank=False,
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '%s %s' % (self.order, self.location)