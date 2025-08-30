from rest_framework import generics
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationListView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).order_by('-updated_at')

class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(conversation_id=conversation_id).order_by('created_at')
    
    def perform_create(self, serializer):
        conversation_id = self.kwargs['conversation_id']
        serializer.save(sender=self.request.user, conversation_id=conversation_id)
