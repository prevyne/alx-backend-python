from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows conversations to be viewed or created.
    """
    queryset = Conversation.objects.all().prefetch_related('participants', 'messages')
    serializer_class = ConversationSerializer

    def get_queryset(self):
        """Optionally filters conversations by the logged-in user."""
        user = self.request.user
        if user.is_authenticated:
            return user.conversations.all().prefetch_related('participants', 'messages')
        return Conversation.objects.none() # Or handle unauthenticated access as needed

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or sent.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        """
        Sets the sender of the message to the currently logged-in user.
        """
        # Ensure the conversation exists before saving the message
        conversation_id = self.request.data.get('conversation')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise serializers.ValidationError("Conversation not found.")
            
        serializer.save(sender=self.request.user, conversation=conversation)