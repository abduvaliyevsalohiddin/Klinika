from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *


class BemorlarAPI(APIView):
    def get(self, request):
        bemorlar = Bemor.objects.all().order_by("-id")
        ism = request.query_params.get("ism")
        tel = request.query_params.get("tel")
        if ism:
            bemorlar = bemorlar.filter(ism__contains=ism)
        if tel:
            bemorlar = bemorlar.filter(tel__contains=tel)
        serializer = BemorSerializer(bemorlar, many=True)
        return Response(serializer.data)


class YollanmalarAPI(APIView):
    def get(self, request):
        yollanmalar = Yollanma.objects.all()
        serializer = YollanmaSerializer(yollanmalar, many=True)
        return Response(serializer.data)

    def post(self, request):
        yollanma = request.data
        serializer = YollanmaSerializer(data=yollanma)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
