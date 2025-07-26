from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated # Import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsParticipantOfConversation # Import your custom permission
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter

class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows conversations to be viewed or created.
    """
    serializer_class = ConversationSerializer
    # Apply permissions: Must be logged in AND a participant.
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """Filters conversations to only those the user is a part of."""
        return self.request.user.conversations.all().prefetch_related('participants', 'messages')

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for messages within a specific conversation.
    """
    serializer_class = MessageSerializer
    # Apply permissions: Must be logged in AND a participant of the parent conversation.
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        """
        This view returns a list of all messages for the conversation
        as determined by the conversation_pk portion of the URL.
        """
        conversation_pk = self.kwargs['conversation_pk']
        conversation = get_object_or_404(Conversation, pk=conversation_pk)
        # Manually check object permission for the parent conversation
        self.check_object_permissions(self.request, conversation)
        return Message.objects.filter(conversation=conversation)

    def perform_create(self, serializer):
        """
        Associates the message with the conversation from the URL.
        """
        conversation_pk = self.kwargs['conversation_pk']
        conversation = get_object_or_404(Conversation, pk=conversation_pk)
        # Manually check object permission before creating the message
        self.check_object_permissions(self.request, conversation)
        serializer.save(sender=self.request.user, conversation=conversation)