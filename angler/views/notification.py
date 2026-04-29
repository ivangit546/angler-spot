from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from angler.models.notification import Notification
from angler.models.post import Comment, Like
from angler.models.friends import FriendRequest

class NotificationView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        like_ct = ContentType.objects.get_for_model(Like)
        comment_ct = ContentType.objects.get_for_model(Comment)
        friendrequest_ct = ContentType.objects.get_for_model(FriendRequest)
        
        all_notifications = (Notification.objects.filter(recipient=request.user, is_read=False, content_type=like_ct).order_by('-created_at') |
                             Notification.objects.filter(recipient=request.user, is_read=False, content_type=comment_ct).order_by('-created_at') |
                             Notification.objects.filter(recipient=request.user, is_read=False, content_type=friendrequest_ct).order_by('-created_at')
                             ).order_by('-created_at')
        return render(request, 'angler/notifications.html', {'all_notifications': all_notifications})

class ReadNotificationView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, notification_id):
        notification = get_object_or_404(Notification, recipient=request.user, id=notification_id)
        notification.is_read = True
        notification.save()
        return redirect(notification.get_notification_url())

           
        