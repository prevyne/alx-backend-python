from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include the API routes from the 'chats' app under the 'api/' path
    path('api/', include('chats.urls')),
    # Add DRF's login/logout views for the browsable API
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]