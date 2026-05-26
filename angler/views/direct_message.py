from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from angler.models.user import User
from angler.models.chat import GroupChat, DirectMessage, Reaction
from angler.models.notification import Notification
from django.db.models import Q
from angler.forms.direct_meesage import DirectMessageCreateForm
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.forms import modelform_factory
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch


class CreateGroupChat(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, user_id):
        user_to_message = get_object_or_404(User, id=user_id)
        existing_gc_1 = GroupChat.objects.filter(owner=request.user, users=user_to_message, deleted_at=None).annotate(user_count=Count('users')).filter(user_count=1).first()
        existing_gc_2 = GroupChat.objects.filter(owner=user_to_message, users=request.user, deleted_at=None).annotate(user_count=Count('users')).filter(user_count=1).first()

        if existing_gc_1:
            return redirect('direct_message', gc_id=existing_gc_1.id)
        elif existing_gc_2:
            return redirect('direct_message', gc_id=existing_gc_2.id)
        else:    
            group_chat = GroupChat.objects.create(owner=request.user)
            group_chat.set_default_image()
            group_chat.group_name = group_chat.owner.get_profile_name
            group_chat.save()
            group_chat.users.add(user_to_message)
            notification_msg = f"@{group_chat.owner.username} has started a chat with you"
            Notification.objects.create(recipient=user_to_message, sender=group_chat.owner, message=notification_msg, content_object=group_chat)
        context = {
            'group_chat':group_chat
        }
        return render(request, 'angler/direct_message/chatbox.html', context)


class ChatListView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        group_chats = GroupChat.objects.filter(Q(owner=request.user)| Q(users=request.user), deleted_at=None).distinct().annotate(
            unread_count=Count(
                'notifications',
                filter=Q(
                    notifications__recipient=request.user,
                    notifications__is_read=False
                ), distinct=True
            )
        )

        context = {
            'group_chats':group_chats
        }
        return render(request, 'angler/direct_message/chat_list.html', context)

class ChatView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, gc_id):
        group_chat = GroupChat.objects.filter(
            Q(users=request.user) | Q(owner=request.user),
            id=gc_id,
            deleted_at=None
        ).distinct().first()

        if not group_chat:
            raise Http404('Invalid request, group chat does not exist')
        chat_messages_query = group_chat.chat_messages.order_by('created_at')[:50]
        form = DirectMessageCreateForm()
        messages_with_reactions = []
        for message in chat_messages_query:
            reactions = message.reaction.values('reaction').annotate(count=Count('reaction'))
            messages_with_reactions.append((message, reactions))

        EditGroupChatForm = modelform_factory(GroupChat, fields=['group_name', 'image',])
        gc_content_type = ContentType.objects.get_for_model(GroupChat)
        Notification.objects.filter(recipient=request.user, is_read=False, content_type=gc_content_type, object_id=group_chat.id).update(is_read=True)

        context = {
            'group_chat':group_chat,
            'messages_with_reactions': messages_with_reactions,
            'form':form,
            'reaction_choices': Reaction.REACTION_CHOICES,
            'edit_form':EditGroupChatForm(instance=group_chat)
        }
        return render(request, 'angler/direct_message/chatbox.html', context)
    
    
    def post (self, request, gc_id):
        group_chat = GroupChat.objects.filter(
            Q(users=request.user) | Q(owner=request.user),
            id=gc_id,
            deleted_at=None
            ).distinct().first()
        if not group_chat:
            raise Http404('Invalid request, group chat does not exist')
        
        reply_id = request.POST.get('reply_to')
        parent_message = None
        if reply_id:
            parent_message = get_object_or_404(DirectMessage, id=reply_id)
        form = DirectMessageCreateForm(request.POST, request.FILES)
        if form.is_valid:
            chat_message = form.save(commit=False)
            chat_message.author = request.user
            chat_message.group = group_chat
            if reply_id:
                chat_message.parent = parent_message
            chat_message.save()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'chat_{gc_id}',
                {
                    'type': 'chat_message',
                    'message_id': chat_message.id,
                    'text': chat_message.text or '',
                    'author_id': request.user.id,
                    'author_name': request.user.get_profile_name,
                    'author_username': request.user.username,
                    'author_image': request.user.get_profile_image().url,
                    'image_url': chat_message.image.url if chat_message.image else None,
                    'parent': None,
                }
            )
            message_recipients = group_chat.users.exclude(id=chat_message.author.id)
            if group_chat.owner != chat_message.author:
                message_recipients = (message_recipients | group_chat.owner)
                notification_msg = f"@{group_chat.owner.username} has sent you a message"
                for user in message_recipients:        
                    Notification.objects.create(recipient=user, sender=chat_message.author, message=notification_msg, content_object=group_chat)
            return JsonResponse({'status': 'ok'})    
        return JsonResponse({'status': 'error'}, status=400)

class GroupChatAddView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, gc_id):
        group_chat = GroupChat.objects.filter(
            Q(users=request.user) | Q(owner=request.user),
            id=gc_id,
            deleted_at=None
            ).distinct().first()
        if not group_chat:
            raise Http404('Invalid request, group chat does not exist')
        if request.user != group_chat.owner:
            raise Http404('Invalid request, only group chat owner can add users')  
        username = request.POST.get('username')
        try:
            user_to_add = User.objects.get(username=username)
            if group_chat.owner != user_to_add and not GroupChat.objects.filter(id=gc_id, users=user_to_add).exists():
                try:
                    group_chat.users.add(user_to_add)
                    notification_msg = f"you have been added to a group chat"
                    Notification.objects.create(recipient=user_to_add, sender=request.user, message=notification_msg, content_object=group_chat)
                    return JsonResponse({'status': 'ok'})
                except ValueError as e:
                    return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': f'@{username} does not exist.'})

        return redirect('direct_message', gc_id=group_chat.id)

class GroupChatEditView(LoginRequiredMixin, View):
    login_url = '/login/'
    EditGroupChatForm = modelform_factory(GroupChat, fields=['group_name', 'image',])

    def post(self, request, gc_id):
        group_chat = GroupChat.objects.get(id=gc_id)
        GroupChatForm = modelform_factory(GroupChat, fields=['group_name', 'image'])
        form = GroupChatForm(request.POST, request.FILES, instance=group_chat)
        if form.is_valid():
            gc = form.save()
            return JsonResponse({
                'status': 'ok',
                'group_name': gc.group_name,
                'image_url': gc.image.url if gc.image else None
            })
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

class ReactMessageView(View):
    def post(self, request, message_id):
        reaction_type = request.POST.get('reaction')
        valid_reactions = [choice[0] for choice in Reaction.REACTION_CHOICES]
        
        if reaction_type not in valid_reactions:
            return JsonResponse({'status': 'error'}, status=400)
        
        message = DirectMessage.objects.get(id=message_id)
        content_type = ContentType.objects.get_for_model(DirectMessage)

        Reaction.objects.update_or_create(
            user=request.user,
            content_type=content_type,
            object_id=message.id,
            defaults={'reaction': reaction_type}
        )

        reaction_counts = Reaction.objects.filter(
            content_type=content_type,
            object_id=message.id
        ).values('reaction').annotate(count=Count('reaction'))
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{message.group.id}',
            {
                'type': 'reaction_update',
                'message_id': message_id,
                'reactions': list(reaction_counts),
            }
        )
        return JsonResponse({'status': 'ok'})
    
class LeaveGroupChatView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, gc_id):
        group_chat = GroupChat.objects.filter(
            Q(users=request.user) | Q(owner=request.user),
            id=gc_id,
            deleted_at=None
            ).distinct().first()
        if not group_chat:
            raise Http404('Invalid request, group chat does not exist') 
               
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        if action == 'leave':
            group_chat.leave_group_chat(request.user)
            return redirect('group_chats')
        elif action == 'remove':
            user_to_remove = get_object_or_404(User, id=user_id)
            if request.user != group_chat.owner:
                raise Http404('Invalid request, only group chat owner can remove users')
            group_chat.users.remove(user_to_remove)
            return JsonResponse({'status': 'ok', 'user_id': user_id})
     

           