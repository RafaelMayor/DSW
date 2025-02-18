from shared.decorators import method_required
from shared.utils import custom_404

from .models import Category
from .serializers import CategoriesSerializer


@method_required('GET')
def categories_list(request):
    categories = CategoriesSerializer(Category.objects.all())
    return categories.json_response()


@method_required('GET')
def category_details(request, slug):
    try:
        categories = CategoriesSerializer(Category.objects.get(slug=slug))
    except Category.DoesNotExist:
        return custom_404('Category not found')

    return categories.json_response()
