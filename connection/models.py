from django.db import models

# Create your models here.
class Connection(models.Model):
    ip = models.CharField(max_length=50)
    mac = models.CharField(max_length=17)
    datetime = models.DateTimeField(auto_created=True)
