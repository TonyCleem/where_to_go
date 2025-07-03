from django.db import models

from tinymce.models import HTMLField


class Location(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Название места",
        unique=True,
        )
    short_description = models.TextField(
        blank=True,
        verbose_name='Краткое описание',
    )
    long_description = HTMLField(
        blank=True,
        verbose_name='Полное описание'
        )
    long = models.FloatField(
        verbose_name='Долгота',
        )
    lat = models.FloatField(
        verbose_name='Широта',
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Image(models.Model):
    order = models.IntegerField(
        default=0,
        blank=True,
        db_index=True,
        verbose_name='Порядок',
    )
    image = models.ImageField(
        verbose_name='Изображение',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Локация',
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order} - {self.location}'
