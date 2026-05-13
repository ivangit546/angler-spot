from angler.models.notification import Notification
from angler.models.chat import DirectMessage, GroupChat
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

def notification_counter(request):
    if request.user.is_authenticated:
        message_ct = ContentType.objects.get_for_model(DirectMessage)
        gc_ct = ContentType.objects.get_for_model(GroupChat)
        notification_count = Notification.objects.filter(recipient=request.user, is_read=False).exclude(Q(content_type=message_ct) & Q(content_type=gc_ct)).count()
        if notification_count > 99:
            notification_count = '99+'
        return{
            'notification_count':notification_count
            }
    else:
        return {'none':0}
    
def message_counter(request):
    if request.user.is_authenticated:
        message_ct = ContentType.objects.get_for_model(DirectMessage)
        gc_ct = ContentType.objects.get_for_model(GroupChat)
        message_notification_count = Notification.objects.filter(Q(content_type=message_ct) | Q(content_type=gc_ct), recipient=request.user, is_read=False) 
        if message_notification_count > 99:
            message_notification_count = '99+'
        return{
            'message_notification_count':message_notification_count
            }
    else:
        return {'none':0}
