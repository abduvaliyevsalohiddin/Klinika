from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async

from .models import *
from .serializers import *


class TolovConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("tolov_group", self.channel_name)
        await self.send_all_tolovs()

    async def send_all_tolovs(self):
        tolovlar = await self.hamma_tolovlar()
        await self.send(text_data=json.dumps(tolovlar))

    @sync_to_async()
    def hamma_tolovlar(self):
        tolovlar = Tolov.objects.all()
        serializer = TolovSerializer(tolovlar, many=True)
        return serializer.data

    async def we_have_updates(self, event):
        await self.send_all_tolovs()

    async def disconnect(self, code):
        await self.channel_layer.group_discard("tolov_group", self.channel_name)
