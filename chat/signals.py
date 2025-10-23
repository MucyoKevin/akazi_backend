from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Conversation

User = get_user_model()

@receiver(pre_delete, sender=User)
def cleanup_user_conversations(sender, instance, **kwargs):
    """
    Clean up conversations when a user is deleted.
    Remove the user from all conversations and delete conversations with no remaining participants.
    """
    # Get all conversations where this user is a participant
    conversations = Conversation.objects.filter(participants=instance)
    
    for conversation in conversations:
        # Remove the user from the conversation
        conversation.participants.remove(instance)
        
        # If no participants remain, delete the conversation
        if conversation.participants.count() == 0:
            conversation.delete()




