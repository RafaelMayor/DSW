import json
import re

from django.http import JsonResponse

from users.models import Token


def require_get_method(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        if request.method != 'GET':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        return func(*args, **kwargs)

    return wrapper


def require_post_method(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        if request.method != 'POST':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        return func(*args, **kwargs)

    return wrapper


def validate_json_body(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        try:
            json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)
        return func(*args, **kwargs)

    return wrapper


def gather_fields(*json_fields: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            request = args[0]
            json_body = json.loads(request.body)
            for f in json_fields:
                if f not in json_body.keys():
                    return JsonResponse({'error': 'Missing required fields'}, status=400)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_token(func):
    def wrapper(*args, **kwargs):
        KEY_PATTERN = r'^Bearer ([a-fA-F\d]{8}(?:\-[a-fA-F\d]{4}){3}\-[a-fA-F\d]{12})$'
        request = args[0]
        auth_header = request.headers.get('Authorization')
        if not re.match(KEY_PATTERN, auth_header):
            return JsonResponse({'error': 'Invalid authentication token'}, status=400)
        return func(*args, **kwargs)

    return wrapper


def is_token_registered(func):
    def wrapper(*args, **kwargs):
        KEY_PATTERN = r'^Bearer ([a-fA-F\d]{8}(?:\-[a-fA-F\d]{4}){3}\-[a-fA-F\d]{12})$'
        request = args[0]
        auth_header = request.headers.get('Authorization')
        token = re.match(KEY_PATTERN, auth_header)
        if token:
            try:
                Token.objects.get(key=token[1])
            except Token.DoesNotExist:
                return JsonResponse({'error': 'Unregistered authentication token'}, status=401)
        return func(*args, **kwargs)

    return wrapper
