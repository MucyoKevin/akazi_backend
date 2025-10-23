from rest_framework import serializers
from .models import Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'content', 'sender', 'sender_name', 'is_read', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = serializers.StringRelatedField(many=True, read_only=True)
    booking_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'booking', 'booking_id', 'messages', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Remove booking_id from validated_data as it's handled in the view
        validated_data.pop('booking_id', None)
        return super().create(validated_data)
