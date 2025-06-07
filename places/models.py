from django.db import models


class Location(models.Model):
    title = models.CharField(
        max_length=200,
        default='',
        blank=True,
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
    description_long = models.TextField(
        default='',
        blank=True,
    )
    long = models.FloatField(
        null=True,
        blank=False,
    )
    lat = models.FloatField(
        null=True,
        blank=False,
    )

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
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return '%s %s' % (self.order, self.location)