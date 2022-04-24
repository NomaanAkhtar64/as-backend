from django.db import models


class Connection(models.Model):
    ip = models.CharField(max_length=50)
    mac = models.CharField(max_length=17)
    datetime = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.ip
