from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'location'

    def __str__(self):
        return self.name
