from rest_framework import serializers

from .models import *


class TolovSerializer(serializers.ModelSerializer):
    class Meta():
        model = Tolov
        fields = '__all__'


class QoshimchaTolovlarSerializer(serializers.ModelSerializer):
    class Meta():
        model = QoshimchaTolov
        fields = '__all__'
