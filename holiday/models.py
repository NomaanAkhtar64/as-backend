from django.db import models


class Holiday(models.Model):
    name = models.CharField(max_length=100)
    repeats = models.BooleanField(default=True)
    date = models.DateField()

    def __str__(self):
        return self.name
