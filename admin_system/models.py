from django.db import models
import base64


DAYS = (
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
)


class WorkingDay(models.Model):
    day_name = models.CharField(max_length=2, choices=DAYS, unique=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.get_day_name_display()


class AdminConfig(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return "Admin Config"

    class Meta:
        verbose_name = "Admin Config"
        verbose_name_plural = "Admin Config"


class Company(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField()
    address = models.TextField()
