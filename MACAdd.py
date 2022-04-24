# import gspread # pip install gspread
# import pyrebase
import os
import re  # regular expression lib
import time
from datetime import datetime, timedelta
from subprocess import Popen, PIPE

from backports.zoneinfo import ZoneInfo
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendance_system.settings")
django.setup()

from django.conf import settings
from connection.models import Connection


def main():
    # The time between ping and arp check must be small, as ARP may not cache longimport
    # Running infinity loop to keep checking the Arp table
    while True:
        pid = Popen(
            ["arp", "-n"], stdout=PIPE
        )  # When the phone connects to hotspot MAC with IP is noted in ARP table
        totalOutput = pid.communicate()[0].decode(
            "ascii"
        )  # This line display the output of arp -n in a varimport csvvariable in lines
        lines = totalOutput.split("\n")
        print(lines)
        for line in lines:
            result = line.find("en0")  # finding device MAC
            # result = line.find("enp3s0")  # finding device MAC
            if result > 0:
                userMACmatches = re.findall(
                    r"(?:[0-9a-fA-F]:?){12}", line
                )  # regular expression for MAC
                userIPmatches = re.findall(
                    r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", line
                )  # regular expression for IP
                if len(userMACmatches) > 0 and len(userIPmatches) > 0:
                    createConnection(userMACmatches[0], userIPmatches[0])
        time.sleep(5)


def createConnection(userMAC, userIP):
    cur = datetime.now(tz=ZoneInfo(settings.TIME_ZONE))
    if (
            Connection.objects.filter(
                mac=userMAC,
                datetime__gte=cur - timedelta(minutes=20),
            ).count()
            # FINDS COUNT OF CONNECTION OBJECTS WITH GIVEN MAC ADDRESS CREATED IN THE LAST 20 MINUTES
            == 0
    ):
        try:
            conn = Connection.objects.get(mac=userMAC)
            conn.ip = userIP
            conn.datetime = cur
            conn.save()

        except Connection.DoesNotExist:
            Connection.objects.create(mac=userMAC, ip=userIP, datetime=cur)

        print(
            f"CREATED CONNECTION MAC: {userMAC} IP: {userIP} date: {cur.date()} time:{cur.time()}"
        )


if __name__ == "__main__":
    """
    This is where the program starts. GPP, as python does not have built-in main function, 
    so we can create our own like this, so that we don't get confused in determining local and global scope.
    """
    main()
