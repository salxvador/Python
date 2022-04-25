from django.contrib import admin
# This is to add our model DB object to the admin page:
from .models import House
admin.site.register(House)
