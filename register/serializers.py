from rest_framework import serializers

from .models import *


class BemorSerializer(serializers.ModelSerializer):
    class Meta():
        model = Bemor
        fields = '__all__'


class YollanmaSerializer(serializers.ModelSerializer):
    class Meta():
        model = Yollanma
        fields = '__all__'
