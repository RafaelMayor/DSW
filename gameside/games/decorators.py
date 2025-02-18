import json
from functools import wraps

from django.http import JsonResponse


def validate_review_data(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)

        rating = data.get('rating', None)
        comment = data.get('comment', None)
        if not rating or not comment:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        if int(rating) < 1 or int(rating) > 5:
            return JsonResponse({'error': 'Rating is out of range'}, status=400)

        return view_func(request, *args, **kwargs)

    return _wrapped_view
