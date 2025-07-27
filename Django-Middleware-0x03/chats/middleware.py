import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden
import time as time_module

# --- Task 1: Request Logging Middleware ---
class RequestLoggingMiddleware:
    """Logs every incoming request to the requests.log file."""
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('request_logger')
        if not self.logger.handlers:
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
    """Restricts API access to standard business hours."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # As per common interpretation, restricts access outside 9 AM to 6 PM.
        now_time = datetime.now().time()
        start_time = time(9, 0)
        end_time = time(18, 0)
        
        if request.path.startswith('/api/'):
            if not (start_time <= now_time <= end_time):
                return HttpResponseForbidden("Access is restricted outside of business hours (9 AM - 6 PM).")
        
        response = self.get_response(request)
        return response

# --- Task 3: Rate Limiting Middleware ---
class OffensiveLanguageMiddleware:
    """
    Implements rate-limiting for sending messages, as per the task instructions.
    Note: The class name is from the prompt; the function is rate-limiting.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_data = {}  # In-memory store for IP tracking

    def __call__(self, request):
        if request.method == 'POST' and '/messages/' in request.path:
            ip_address = request.META.get('REMOTE_ADDR')
            current_time = time_module.time()
            
            if ip_address not in self.requests_data:
                self.requests_data[ip_address] = {'timestamp': current_time, 'count': 1}
            else:
                if current_time - self.requests_data[ip_address]['timestamp'] > 60:
                    self.requests_data[ip_address] = {'timestamp': current_time, 'count': 1}
                else:
                    self.requests_data[ip_address]['count'] += 1

            if self.requests_data[ip_address]['count'] > 5:
                return HttpResponseForbidden("Rate limit exceeded. Please wait before sending more messages.")

        response = self.get_response(request)
        return response

# --- Task 4: Role-Based Permission Middleware ---
class RolePermissionMiddleware:
    """Enforces that only users with the 'admin' role can access API endpoints."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define paths that are exempt from this role check
        exempt_paths = ['/api/', '/api/token/', '/api/token/refresh/']

        if request.path.startswith('/api/') and request.path not in exempt_paths:
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication is required.")
            
            allowed_roles = ['admin']
            if request.user.role not in allowed_roles:
                return HttpResponseForbidden("You do not have the required role (admin) to access this resource.")

        response = self.get_response(request)
        return response