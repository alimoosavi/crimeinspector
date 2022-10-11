from django.db import models


class Crime(models.Model):
    unique_key = models.IntegerField(unique=True)
    primary_type = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    date = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        index_together = ('primary_type', 'date',)
