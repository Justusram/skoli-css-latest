from django.contrib import admin
from .models import Övning, Fråga, Alternativ

# Register your models here.
admin.site.register(Övning)
admin.site.register(Fråga)
admin.site.register(Alternativ)