from django.contrib import admin
from .models import Connection


class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['ip', 'mac', 'datetime']


admin.site.register(Connection, ConnectionAdmin)
