from functools import wraps
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import status
from employee.models import Employee


def check_mac(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not "mac" in request.data:
            return Response(
                "MAC Address not provided", status=status.HTTP_400_BAD_REQUEST
            )

        mac = request.data["mac"]
        if not Employee.verify_mac_address(mac):
            return Response("Invalid MAC Address", status=status.HTTP_400_BAD_REQUEST)

        search = Employee.find_employee(mac)

        if not search.found:
            return Response(
                "You are not an employee", status=status.HTTP_400_BAD_REQUEST
            )

        return function(request, *args, employee=search.employee, **kwargs)

    return wrap
