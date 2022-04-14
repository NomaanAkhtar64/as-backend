import re
from datetime import datetime
from collections import namedtuple
from django.db import models
from django.contrib.auth.models import User

MAC_ADDRESS_REGEX = re.compile(
    "^(((\d|([a-f]|[A-F])){2}:){5}(\d|([a-f]|[A-F])){2})$|^(((\d|([a-f]|[A-F])){2}-){5}(\d|([a-f]|[A-F])){2})$|^$"
)
Search = namedtuple("Search", ["found", "employee"])


class Employee(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    wage_per_hour = models.IntegerField()
    contact_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    joining_date = models.DateField()
    leaving_date = models.DateField(blank=True, null=True, default=None)
    brand_of_device = models.CharField(max_length=150)
    mac_address = models.CharField(max_length=17, unique=True, blank=True, null=True)

    @classmethod
    def verify_mac_address(mac_address):
        return MAC_ADDRESS_REGEX.match(mac_address)

    @classmethod
    def find_employee(mac_address):
        try:
            employee = Employee.objects.get(mac_address=mac_address)
            return Search(True, employee)
        except Employee.DoesNotExist:
            return Search(False, None)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PartialEmployee(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    brand_of_device = models.CharField(max_length=150)
    applied = models.DateField(auto_created=True)
