from django.contrib import admin

# Register your models here.
from .models import Service, Request_type, Requests
# Register your models here.
admin.site.register(Service)
admin.site.register(Request_type)
admin.site.register(Requests)
