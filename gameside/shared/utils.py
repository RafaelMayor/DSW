from django.http import JsonResponse


def custom_404(message):
    return JsonResponse({'error': message}, status=404)


def custom_403(message):
    return JsonResponse({'error': message}, status=403)
