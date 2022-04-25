import re
import datetime as dt
from collections import namedtuple
from backports.zoneinfo import ZoneInfo
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db import models

from connection.models import Connection

MAC_ADDRESS_REGEX = re.compile(
    "^(((\d|([a-f]|[A-F])){2}:){5}(\d|([a-f]|[A-F])){2})$|^(((\d|([a-f]|[A-F])){2}-){5}(\d|([a-f]|[A-F])){2})$|^$"
)
Search = namedtuple("Search", ["found", "employee"])


def get_now_date():
    return dt.datetime.now(tz=ZoneInfo(settings.TIME_ZONE)).date()


class PartialEmployee(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    brand_of_device = models.CharField(max_length=150)
    applied = models.DateField(auto_created=True, default=get_now_date)
    date_of_birth = models.DateField()
    contact = models.CharField(max_length=50)
    ip = models.CharField(max_length=50)


class Employee(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    wage_per_hour = models.FloatField()
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

    def save(self, *arg, **kw) -> None:
        if not self.pk:
            """
            GET MAC ADDRESS BY MATCHING IP
            """
            p_employee = PartialEmployee.objects.get(user=self.user.id)
            try:
                conn = Connection.objects.get(ip=p_employee.ip)
                self.mac_address = conn.mac
            except Connection.DoesNotExist:
                pass
            p_employee.delete()
        return super().save(*arg, **kw)

    def status(self):
        if self.leaving_date is None:
            return "Active"
        if self.leaving_date > dt.datetime.now(tz=ZoneInfo(settings.TIME_ZONE)).date():
            return "Active"
