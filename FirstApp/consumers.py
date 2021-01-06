import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Chat,Room,UserData
from django.contrib.auth import get_user_model
from datetime import datetime
from django.core import serializers
User=get_user_model()
class ChatConsumer(WebsocketConsumer):
    response = {}
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if text_data_json['command'] == 'new_message':
            message = text_data_json['message']
            name = text_data_json['name']

            uname = User.objects.filter(username=name)[0]

            chat = Chat(name=uname, msg=message,room=Room.objects.get(name = text_data_json['room']))
            chat.save()
            udata = UserData.objects.get(user=uname)


            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'name':name,
                    'image_url':udata.Dp.url,
                    'command':text_data_json['command']
                }
            )

        elif text_data_json['command']=="fetch_old":
            messages = []
            msgs = Chat.objects.order_by('-timestamp').filter(room=Room.objects.get(name = text_data_json['room']))

            for m in msgs:
                user = User.objects.get(username= m.name.username)
                udata = UserData.objects.get(user=user)
                messages.append({'name': m.name.username, 'content': m.msg,'image_url':udata.Dp.url,'timestamp':datetime.strftime(datetime.strptime(str(m.timestamp),"%H:%M:%S.%f"),"%I:%M")})
                
                self.response = json.dumps({"messages": messages}, default=str)
           
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'messages':self.response,
                    'command': text_data_json['command'],
                    's_name':text_data_json['name'],
                    
                }
            )

    # Receive message from room group
    def chat_message(self, event):

        command=event['command']
        if(command == 'new_message'):
            message = event['message']
            name = event['name']
            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'message': message,
                'name':name,
                'image_url':event['image_url'],
                'command':command,
            }))

        else:
            self.send(text_data=json.dumps({
                'messages':self.response,
                'command': command,
                's_name':event['s_name'],
                
            }))