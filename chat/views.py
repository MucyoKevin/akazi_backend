from rest_framework import generics, status
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationListView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer
    
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).order_by('-updated_at')
    
    def perform_create(self, serializer):
        # If booking_id is provided, validate it first
        booking_id = self.request.data.get('booking_id')
        if booking_id:
            try:
                from bookings.models import Booking
                booking = Booking.objects.get(id=booking_id)
                # Create conversation with booking
                conversation = serializer.save(booking=booking)
                conversation.participants.add(self.request.user)
                conversation.participants.add(booking.provider.user)
            except Booking.DoesNotExist:
                return Response(
                    {'error': f'Booking with id {booking_id} does not exist'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # Create conversation without booking
            conversation = serializer.save()
            conversation.participants.add(self.request.user)

class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(conversation_id=conversation_id).order_by('created_at')
    
    def perform_create(self, serializer):
        conversation_id = self.kwargs['conversation_id']
        serializer.save(sender=self.request.user, conversation_id=conversation_id)
