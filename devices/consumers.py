import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer


class SendLiveData(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "live_data"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("in receive method")
        # Send message back to client
        await self.send(text_data=json.dumps({'message': "message"}))

    # # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        message = event["message"]

        print(message)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    async def on_message(self, message):
        print("okay")
        await self.send_json(text_data=json.dumps({"message": "message"}))
