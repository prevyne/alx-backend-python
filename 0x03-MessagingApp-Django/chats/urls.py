from django.urls import path, include
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet
from rest_framework.permissions import AllowAny

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Make the API Root view public
router.get_api_root_view().cls.permission_classes = (AllowAny,)

# Update the 'lookup' parameter to match the view's kwargs
conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation_id')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]