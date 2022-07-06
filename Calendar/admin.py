from django.contrib import admin
from .models import *

admin.site.register(Calendar)
admin.site.register(Customer)
admin.site.register(Event)
admin.site.register(Profile)