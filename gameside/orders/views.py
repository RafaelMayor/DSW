from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from games.serializers import GamesSerializer
from shared.decorators import method_required, token_required
from shared.utils import custom_403, custom_404

from .decorators import (
    validate_order_pay_exist,
    validate_order_status_exist,
    validate_orders_games_add_data,
    validate_pay_data,
    validate_status_data,
)
from .models import Order
from .serializers import OrdersSerializer


@method_required('POST')
@token_required
def order_add(request):
    user = request.user
    order = Order.objects.create(user=user)
    return JsonResponse({'id': order.pk}, status=200)


@method_required('GET')
@token_required
def order_details(request, pk):
    user = request.user
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return custom_404('Order not found')
    if order.user != user:
        return custom_403('User is not the owner of requested order')
    order_ = OrdersSerializer(order, request=request)
    return JsonResponse(order_.serialize(), safe=False)


@method_required('GET')
@token_required
def order_games(request, pk):
    user = request.user
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return custom_404('Order not found')
    if order.user != user:
        return custom_403('User is not the owner of requested order')
    games = GamesSerializer(order.games.all(), request=request)
    return JsonResponse(games.serialize(), safe=False)


@method_required('POST')
@validate_orders_games_add_data
@token_required
def order_games_add(request, pk):
    user = request.user

    order = request.order
    game = request.game
    if order.user != user:
        return custom_403('User is not the owner of requested order')

    order.games.add(request.game)
    game.stock = game.stock - 1
    game.save()
    return JsonResponse({'num-games-in-order': order.games.count()}, safe=False)


@method_required('POST')
@validate_status_data
@token_required
@validate_order_status_exist
def order_status(request, pk):
    order = request.order
    status = request.status
    user = request.user
    if order.user != user:
        return custom_403('User is not the owner of requested order')
    order.status = status
    order.save()
    return JsonResponse({'status': order.get_status_display()}, safe=False)


@csrf_exempt
@method_required('POST')
@validate_pay_data
@token_required
@validate_order_pay_exist
def order_pay(request, pk):
    order = request.order
    order.status = Order.Status.PAID
    order.save()
    return JsonResponse({'status': order.get_status_display(), 'key': order.key}, safe=False)
