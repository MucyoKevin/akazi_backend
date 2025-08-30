from .models import Notification

def send_notification(user, title, message, notification_type='reminder'):
    """
    Utility function to create and send notifications to users
    """
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type
    )
    return notification
