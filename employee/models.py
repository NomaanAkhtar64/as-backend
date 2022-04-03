import re
from datetime import datetime
from collections import namedtuple
from django.db import models

MAC_ADDRESS_REGEX = re.compile(
    "^(((\d|([a-f]|[A-F])){2}:){5}(\d|([a-f]|[A-F])){2})$|^(((\d|([a-f]|[A-F])){2}-){5}(\d|([a-f]|[A-F])){2})$|^$"
)
Search = namedtuple("Search", ["found", "employee"])


class Employee(models.Model):
    name = models.CharField(max_length=100)
    gross_salary = models.IntegerField()
    mac_address = models.CharField(max_length=17, unique=True)

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
        return self.name
