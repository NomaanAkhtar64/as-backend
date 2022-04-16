from rest_framework import serializers


class MonthAttendance:
    def __init__(self, year, month, hours_worked):
        self.year = year
        self.month = month
        self.hours_worked = hours_worked


class MonthAttendanceSerializer(serializers.Serializer):
    year = serializers.CharField(max_length=4)
    month = serializers.CharField(max_length=2)
    hours_worked = serializers.IntegerField()


class YearAttendance:
    def __init__(self, year, hours_worked):
        self.year = year
        self.hours_worked = hours_worked


class YearAttendanceSerializer(serializers.Serializer):
    year = serializers.CharField(max_length=4)
    hours_worked = serializers.IntegerField()
