import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden
import time as time_module

# --- Task 1: Request Logging Middleware ---
class RequestLoggingMiddleware:
    """Logs every incoming request to a file."""
    def __init__(self, get_response):
        self.get_response = get_response
        # Set up a dedicated logger for requests
        self.logger = logging.getLogger('request_logger')
        handler = logging.FileHandler('requests.log')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'AnonymousUser'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)
        
        response = self.get_response(request)
        return response

# --- Task 2: Time Restriction Middleware ---
class RestrictAccessByTimeMiddleware:
    """Restricts access to the API outside of specified hours."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # The prompt specifies "9PM and 6PM". This is interpreted as restricting
        # access outside the standard business hours of 9 AM to 6 PM.
        now_time = datetime.now().time()
        start_time = time(9, 0)   # 9 AM
        end_time = time(18, 0)  # 6 PM
        
        # Only apply this restriction to API paths to avoid blocking admin/static files
        if request.path.startswith('/api/'):
            if not (start_time <= now_time <= end_time):
                return HttpResponseForbidden("Access is restricted outside of business hours (9 AM - 6 PM).")
        
        response = self.get_response(request)
        return response

# --- Task 3: Rate Limiting Middleware ---
class OffensiveLanguageMiddleware:
    """
    Implements rate-limiting for sending messages as per instructions.
    Note: The class name is per the prompt, but the function is rate-limiting.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_data = {}  # In-memory store: {'ip': {'timestamp': float, 'count': int}}

    def __call__(self, request):
        # Only rate-limit POST requests to message creation endpoints
        if request.method == 'POST' and '/messages/' in request.path:
            ip_address = request.META.get('REMOTE_ADDR')
            current_time = time_module.time()
            
            # Use a tuple as a key for IP and path to be more specific
            key = (ip_address, request.path)
            
            if key not in self.requests_data:
                self.requests_data[key] = {'timestamp': current_time, 'count': 1}
            else:
                # If the last request was more than a minute ago, reset the counter
                if current_time - self.requests_data[key]['timestamp'] > 60:
                    self.requests_data[key] = {'timestamp': current_time, 'count': 1}
                else:
                    self.requests_data[key]['count'] += 1

            # Block if the count exceeds the limit (5 messages per minute)
            if self.requests_data[key]['count'] > 5:
                return HttpResponseForbidden("Rate limit exceeded. Please wait a moment before sending more messages.")

        response = self.get_response(request)
        return response

# --- Task 4: Role-Based Permission Middleware ---
class RolePermissionMiddleware:
    """Checks for a specific user role before allowing access to the API."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define specific paths that should be exempt from this role check.
        exempt_paths = ['/api/', '/api/token/', '/api/token/refresh/']

        # Check if the request path starts with /api/ but is NOT one of the exempt paths.
        if request.path.startswith('/api/') and request.path not in exempt_paths:
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication is required.")
            
            allowed_roles = ['admin']
            if request.user.role not in allowed_roles:
                return HttpResponseForbidden("You do not have the required role (admin) to perform this action.")

        response = self.get_response(request)
        return response