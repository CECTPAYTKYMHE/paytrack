from calendar import Calendar
from rest_framework import serializers
from .models import *


class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = '__all__'