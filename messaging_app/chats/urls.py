from django.urls import path, include
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet

# Creating a parent router for Conversations
router = routers.SimpleRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Creating a nested router for Messages, registered under Conversations
conversations_router = routers.NestedSimpleRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]