from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from angler.models.chat import GroupChat, DirectMessage

class ChatroomConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.gc_id = self.scope['url_route']['kwargs']['gc_id']
        self.room_group_name = f"chat_{self.gc_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive_json(self, content):
        user = self.scope['user']
        text = content.get('text')
        reply_to_id = content.get('reply_to')

        message, author_name, author_image, parent_data = await self.save_message(user, text, reply_to_id)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_id': message.id,
                'text': text,
                'author_id': user.id,
                'author_name': author_name,
                'author_username': user.username,
                'author_image': author_image,
                'reply_to': reply_to_id,
                'parent': parent_data,
            }
        )

    @database_sync_to_async
    def save_message(self, user, text, reply_to_id):
        group_chat = GroupChat.objects.get(id=self.gc_id)
        parent = None
        parent_data = None
        if reply_to_id:
            parent = DirectMessage.objects.get(id=reply_to_id)
            parent_data = {
                'author_name': parent.author.get_profile_name,
                'author_image': parent.author.get_profile_image().url,
                'text': parent.text,
            }
        message = DirectMessage.objects.create(
            group=group_chat,
            author=user,
            text=text,
            parent=parent
        )
        author_name = user.get_profile_name
        author_image = user.get_profile_image().url
        return message, author_name, author_image, parent_data

    async def chat_message(self, event):
        await self.send_json(event)

    async def reaction_update(self, event):
        await self.send_json(event)