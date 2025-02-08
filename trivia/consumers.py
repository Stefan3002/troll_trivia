# myapp/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer, channel_layers
from django.core.cache import cache

import trivia.views
from trivia.views import questions, questions_trolled

questions_advanced_1 = 0
questions_advanced_2 = 0

class PlayConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract room name from URL route parameters
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print(self.room_name)
        self.room_group_name = f'play_{self.room_name}'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()
        print('connected')

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive a message from the WebSocket
    async def receive(self, text_data):
        global questions_advanced_1, questions_advanced_2

        print('received')
        data = json.loads(text_data)
        message = data.get('message', '')

        if message['type'] == 'question':
            checked_answer = int(message.get('checkedAnswer', -1))
            question_number = message.get('questionNumber', 0)

            cache_data = cache.get('trolled')
            trolled = False
            if cache_data:
                cache_data_json = json.loads(cache_data)
                print(cache_data_json)
                if self.room_name == cache_data_json['room']:
                    trolled = cache_data_json['trolled']
                else:
                    trolled = False
            if not trolled:
                if questions[question_number]['correct'] == checked_answer :
                    await self.send(text_data=json.dumps({
                        'message': {
                            'type': 'answer',
                            'data': True
                        }

                    }))
                else:
                    await self.send(text_data=json.dumps({
                         'message': {
                            'type': 'answer',
                            'data': False
                        }
                    }))
            else:
                if questions_trolled[question_number]['correct'] == checked_answer:
                    await self.send(text_data=json.dumps({
                        'message': {
                            'type': 'answer',
                            'data': True
                        }

                    }))
                else:
                    await self.send(text_data=json.dumps({
                        'message': {
                            'type': 'answer',
                            'data': False
                        }
                    }))
            return
        if message['type'] == 'troll':
            data = {
                'room': self.room_name,
                'trolled': True
            }
            cache.set('trolled', json.dumps(data))
            # trivia.views.trolled = True
        # Broadcast the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'play_message',
                'message': message
            }
        )

    # Handler for messages sent to the room group
    async def play_message(self, event):
        message = event['message']

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
