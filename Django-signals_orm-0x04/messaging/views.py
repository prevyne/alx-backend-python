from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from .models import Message

# Task 2: View for deleting a user account
@login_required
def delete_user_account(request):
    user_to_delete = request.user
    if request.method == 'POST':
        user_to_delete.delete() # This triggers the post_delete signal
        return HttpResponse("Your account has been successfully deleted.")
    return render(request, 'confirm_delete.html') # A confirmation template is best practice

# Task 3: View demonstrating advanced ORM for threaded conversations
def conversation_thread_view(request, message_id):
    # Use select_related for ForeignKeys and prefetch_related for reverse FKs/M2M
    # This avoids the N+1 query problem by fetching related objects in efficient queries.
    top_message = Message.objects.select_related('sender').prefetch_related('replies__sender').get(id=message_id)
    return render(request, 'conversation_thread.html', {'message': top_message})

# Task 4: View using the custom manager to show an inbox
@login_required
def user_inbox_view(request):
    current_user = request.user
    unread_messages = Message.unread.filter(receiver=current_user).only('id', 'sender__username', 'content')
    
    all_messages = Message.objects.filter(receiver=current_user).select_related('sender')
    
    return render(request, 'inbox.html', {
        'unread_messages': unread_messages,
        'all_messages': all_messages
    })

# Task 5: View with basic caching
@cache_page(60) # Cache this view's output for 60 seconds
def message_list_view(request):
    messages = Message.objects.all().select_related('sender', 'receiver')
    return render(request, 'message_list.html', {
        'messages': messages,
        'info': 'This page is cached and will refresh every 60 seconds.'
    })