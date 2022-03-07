from django.contrib import admin
# standard registration: import the class, then 'admin.site.register()' it:
from .models import djangoClasses

admin.site.register(djangoClasses)
