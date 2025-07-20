from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the custom User model."""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role']

class MessageSerializer(serializers.ModelSerializer):
    """Serializer for the Message model."""
    sender = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Message
        fields = ['id', 'sender', 'message_body', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model, with nested messages.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True
    )

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'participant_ids', 'messages', 'created_at']

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids')
        participants = User.objects.filter(id__in=participant_ids)

        if len(participants) != len(participant_ids):
            raise serializers.ValidationError("One or more participant IDs are invalid.")

        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation