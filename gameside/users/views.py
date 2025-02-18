from django.http import JsonResponse

from shared.decorators import method_required, register_required


@method_required('POST')
@register_required
def auth(request):
    return JsonResponse({'token': request.user.token.key}, safe=False)
