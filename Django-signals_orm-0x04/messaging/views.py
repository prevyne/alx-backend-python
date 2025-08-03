from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from .models import Message

# Task 2: View for deleting a user account
@login_required
def delete_user_account(request):
    """
    Handles the request for a user to delete their own account.
    The user's deletion will trigger the post_delete signal.
    """
    user_to_delete = request.user
    if request.method == 'POST':
        user_to_delete.delete() 
        return HttpResponse("Your account and all associated data have been successfully deleted.")
    
    # In a real application, you would render a confirmation template.
    return render(request, 'messaging/confirm_delete.html')

# Task 3: Example view demonstrating advanced ORM for threaded conversations
def conversation_thread_view(request, message_id):
    """
    Displays a message and its replies, optimized with prefetch_related.
    This avoids the N+1 query problem by fetching related objects efficiently.
    """
    try:
        top_message = Message.objects.select_related('sender').prefetch_related('replies__sender').get(id=message_id)
    except Message.DoesNotExist:
        return HttpResponse("Message not found.", status=404)
        
    return render(request, 'messaging/conversation_thread.html', {'message': top_message})

# Task 4: Example view using the custom manager for a user's inbox
@login_required
def user_inbox_view(request):
    """
    Displays a user's inbox, showing all messages and a special section 
    for unread messages using the custom manager and .only() for optimization.
    """
    current_user = request.user
    
    # Use the custom manager `unread` to get only unread messages for the user.
    unread_messages = Message.unread.filter(receiver=current_user).only('id', 'sender__username', 'content', 'timestamp')

    # Get all messages for the main inbox view.
    all_messages = Message.objects.filter(receiver=current_user).select_related('sender')

    return render(request, 'messaging/inbox.html', {
        'unread_messages': unread_messages,
        'all_messages': all_messages
    })

# Task 5: Example view with basic caching
@cache_page(60) # Cache this view's output for 60 seconds
def message_list_view(request):
    """
    A view that displays a list of all messages in the system.
    The output of this view will be cached to improve performance.
    """
    messages = Message.objects.all().select_related('sender', 'receiver')
    return render(request, 'messaging/message_list.html', {'messages': messages})