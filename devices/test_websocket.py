from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()


def process_message(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'live_data',
        {
            'type': 'chat_message',
            'message': message
        }
    )