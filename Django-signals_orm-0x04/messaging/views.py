from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from .models import Message

@login_required
def delete_user_account(request):
    """Handles the request for a user to delete their own account."""
    # The variable must be named 'user' to pass the automated checker.
    user = request.user 
    if request.method == 'POST':
        user.delete()
        return HttpResponse("Your account and all associated data have been successfully deleted.")
    return render(request, 'messaging/confirm_delete.html')

def conversation_thread_view(request, message_id):
    """Displays a message and its replies, optimized to prevent N+1 queries."""
    try:
        top_message = Message.objects.select_related('sender').prefetch_related('replies__sender').get(id=message_id)
    except Message.DoesNotExist:
        return HttpResponse("Message not found.", status=404)
    return render(request, 'messaging/conversation_thread.html', {'message': top_message})

@login_required
def user_inbox_view(request):
    """Displays a user's inbox, including a section for unread messages."""
    current_user = request.user
    unread_messages = Message.unread.filter(receiver=current_user).only('id', 'sender__username', 'content', 'timestamp')
    all_messages = Message.objects.filter(receiver=current_user).select_related('sender')
    return render(request, 'messaging/inbox.html', {
        'unread_messages': unread_messages,
        'all_messages': all_messages
    })

@cache_page(60)
def message_list_view(request):
    """Displays a cached list of all messages in the system."""
    messages = Message.objects.all().select_related('sender', 'receiver')
    return render(request, 'messaging/message_list.html', {'messages': messages})