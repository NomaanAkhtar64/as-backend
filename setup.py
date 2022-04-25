import os
import django
import datetime
import subprocess
from backports.zoneinfo import ZoneInfo

command_to_execute = ["echo", "Test"]


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendance_system.settings")
django.setup()


from admin_system.models import WorkingDay, AdminConfig, Company
from django.conf import settings
from django.contrib.auth import get_user_model

cmds = [
    ["python3", "manage.py", "makemigrations"],
    ["python3", "manage.py", "migrate"],
]

User = get_user_model()


def main():
    for cmd in cmds:
        print(f'Executing {" ".join(cmd)}')
        run = subprocess.run(cmd, capture_output=True)
        print(run.stdout.decode("utf-8"))
        if run.stderr:
            print(run.stderr.decode("utf-8"))

    if User.objects.filter(is_superuser=True).count() == 0:
        User.objects.create_superuser("test", "test@test.com", "test")
        print("CREATED SUPER USER")

    if WorkingDay.objects.count() == 0:
        for i in range(1, 6):
            WorkingDay.objects.create(day=f"{i}")
        print("CREATED WORKING DAYS")

    if AdminConfig.objects.count() == 0:
        AdminConfig.objects.create(
            start_time=datetime.time(8, 0, tzinfo=ZoneInfo(settings.TIME_ZONE)),
            end_time=datetime.time(16, 0, tzinfo=ZoneInfo(settings.TIME_ZONE)),
        )
        print("CREATED WORKING TIMINGS")

    if Company.objects.count() == 0:
        Company.objects.create(
            name="Test Company",
            address="Building No, Street No, Area, City, State, Country.",
            logo="defaultlogo.png",
        )
        print("CREATED COMPANY DATA")


if __name__ == "__main__":
    main()
