from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Sum
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from xonalar.models import Joylashtirish
from register.models import Bemor
from .models import *
from .serializers import *


class TolovlarAPIView(APIView):
    filter_backends = [SearchFilter]
    search_fields = ['sana', 'tolangan_sana', 'bemor__ism', 'tolandi', 'yollanma__nom', 'yollanma__qayerga']

    def get(self, request):
        tolovlar = Tolov.objects.order_by("-id")
        turi = request.query_params.get("turi")
        if turi == 'yollanma':
            tolovlar = tolovlar.filter(yollanma__isnull=False)
        elif turi == 'joylashtirish':
            tolovlar = tolovlar.filter(joylashtirish__isnull=False)
        serializer = TolovSerializer(tolovlar, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TolovSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "tolov_group",
                {
                    "type": "we_have_updates"
                },
            )
            return Response(serializer.data)
        return Response(serializer.errors)


class TolovAPIView(APIView):
    def put(self, request, pk):
        serializer = TolovSerializer(Tolov.objects.get(id=pk), data=request.data)
        if serializer.is_valid():
            serializer.save()

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "tolov_group",
                {
                    "type": "we_have_updates"
                },
            )
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        Tolov.objects.filter(id=pk).delete()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "person_group",
            {
                "type": "add_new_person",
            },
        )

        return Response({"success": " True", "message": "Tolov o`chirildi"})


class TolovlarAdminAPIView(APIView):
    def get(self, request):
        tolovlar = Tolov.objects.all()
        sana = request.query_params.get('sana')
        bosh_sana = request.query_params.get('bosh_sana')
        yakun_sana = request.query_params.get('yakun_sana')
        if sana:
            tolovlar = Tolov.objects.filter(sana=sana) | Tolov.objects.filter(tolangan_sana=sana)
        if bosh_sana and yakun_sana:
            tolovlar = Tolov.objects.filter(sana__range=[bosh_sana, yakun_sana]) | Tolov.objects.filter(
                tolangan_sana__range=[bosh_sana, yakun_sana])
        serializer = TolovSerializer(tolovlar, many=True)
        tushum = tolovlar.aggregate(s=Sum("tolangan_summa")).get("s")
        if tushum is None:
            tushum = 0
        qarz = tolovlar.aggregate(s=Sum("summa")).get("s")
        if qarz is None:
            qarz = 0
        else:
            qarz -= tushum
        result = {
            "tolovlar": serializer.data,
            "umumiy_tushum": tushum,
            "qarzdorlik": qarz
        }
        return Response(result)


class TolovAPI(APIView):
    def put(self, request, pk):
        tolov = Tolov.objects.get(id=pk)
        serializer = TolovSerializer(tolov, data=request.data)
        if serializer.is_valid():
            serializer.save(
                tolandi=serializer.data.get("tolangan_summa") == serializer.data.get("summa")
            )
            return Response(serializer.data)
        return Response(serializer.errors)


class QoshimchaTolovlarAPIView(APIView):
    def get(self, request):
        qoshimcha_tolovlar = QoshimchaTolov.objects.order_by("-id")
        serializer = QoshimchaTolovlarSerializer(qoshimcha_tolovlar, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = QoshimchaTolovlarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tolov__tolandi=True if serializer.data.get("tolov__tolangan_summ") + serializer.data.get(
                "summa") == serializer.data.get("tolov__summa") else False)
