import json
import re
from functools import wraps

from django.contrib.auth import authenticate
from django.http import JsonResponse

from users.models import Token


def method_required(method):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.method != method:
                return JsonResponse({'error': 'Method not allowed'}, status=405)
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def register_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)

        username = data.get('username', None)
        password = data.get('password', None)
        if not username or not password:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        if user := authenticate(request, username=username, password=password):
            request.user = user
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({'error': 'Authorization token is missing'}, status=403)

        m = re.fullmatch(
            r'Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})',
            token,
        )

        if not m:
            return JsonResponse({'error': 'Invalid authentication token'}, status=400)

        try:
            token_obj = Token.objects.get(key=m['token'])
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

        request.user = token_obj.user
        return view_func(request, *args, **kwargs)

    return _wrapped_view
