from django.urls import path, include
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet

# Use DefaultRouter for the parent to get the API root view
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Use NestedDefaultRouter for the child messages
conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]