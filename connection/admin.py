from django.contrib import admin
from .models import Connection


class ConnectionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Connection, ConnectionAdmin)
