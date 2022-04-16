from django.db import models

HOLIDAY_TYPE = [("Half Day", "Half Day"), ("Full Day", "Full Day")]
REPEATS_TYPE = [("Yearly", "Yearly"), ("Monthly", "Monthly"), ("Once", "Once")]


class Holiday(models.Model):
    name = models.CharField(max_length=100)
    repeats = models.CharField(max_length=32, choices=REPEATS_TYPE)
    date = models.DateField()
    type = models.CharField(max_length=32, choices=HOLIDAY_TYPE)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.name
