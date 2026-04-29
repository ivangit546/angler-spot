from angler.models.notification import Notification

def notification_counter(request):
    if request.user.is_authenticated:
        notification_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        if notification_count > 99:
            notification_count = '99+'
        return{
            'notification_count':notification_count
        }
    else:
        return {'none':0}