from django.db import models

DAYS = (
    ("MN", "Monday"),
    ("TU", "Tuesday"),
    ("WD", "Wednesday"),
    ("TH", "Thursday"),
    ("FR", "Friday"),
    ("ST", "Saturday"),
    ("SN", "Sunday"),
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
