from django.db import models


class Location(models.Model):
    title = models.CharField(
        max_length=200,
        default='',
        blank=True,
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