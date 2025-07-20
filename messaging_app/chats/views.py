from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404

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
        return Conversation.objects.none()

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for messages within a specific conversation.
    Accessed via /conversations/{conversation_pk}/messages/
    """
    serializer_class = MessageSerializer

    def get_queryset(self):
        """
        This view should return a list of all the messages for
        the conversation as determined by the conversation_pk portion of the URL.
        """
        return Message.objects.filter(conversation=self.kwargs['conversation_pk'])

    def perform_create(self, serializer):
        """
        Associates the message with the conversation from the URL
        and sets the sender to the currently logged-in user.
        """
        conversation = get_object_or_404(Conversation, pk=self.kwargs['conversation_pk'])
        serializer.save(sender=self.request.user, conversation=conversation)