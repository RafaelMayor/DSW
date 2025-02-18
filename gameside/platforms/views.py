from django.http import JsonResponse

from shared.decorators import method_required
from shared.utils import custom_404

from .models import Platform
from .serializers import PlatformSerializer


@method_required('GET')
def platorms_list(request):
    platform = Platform.objects.all()
    serializes_platform = PlatformSerializer(platform, request=request)

    return JsonResponse(serializes_platform.serialize(), safe=False)


@method_required('GET')
def platform_details(request, slug):
    try:
        platform = Platform.objects.get(slug=slug)
    except Platform.DoesNotExist:
        return custom_404('Platform not found')

    serializes_platform = PlatformSerializer(platform, request=request)

    return JsonResponse(serializes_platform.serialize(), safe=False)
