import json
import re
from datetime import datetime
from functools import wraps

from django.http import JsonResponse

from games.models import Game
from orders.models import Order


def validate_orders_games_add_data(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)

        game_slug = data.get('game-slug', None)
        if not game_slug:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        pk = kwargs.get('pk')
        if not pk:
            return JsonResponse({'error': 'Order ID is missing'}, status=400)

        try:
            order = Order.objects.get(id=pk)
            request.order = order
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        try:
            game = Game.objects.get(slug=game_slug)
            request.game = game
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status=404)

        if game.stock == 0:
            return JsonResponse({'error': 'Game out of stock'}, status=400)

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def validate_status_data(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)

        status = data.get('status', None)
        if not status:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        pk = kwargs.get('pk')
        if not pk:
            return JsonResponse({'error': 'Order ID is missing'}, status=400)

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def validate_order_status_exist(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        data = json.loads(request.body)
        status = data.get('status', None)
        pk = kwargs.get('pk')
        try:
            order = Order.objects.get(id=pk)
            request.order = order
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        if status not in Order.Status.values:
            return JsonResponse({'error': 'Invalid status'}, status=400)
        if status == Order.Status.INITIATED:
            return JsonResponse({'error': 'Invalid status'}, status=400)
        if status == Order.Status.PAID and order.status != Order.Status.CONFIRMED:
            return JsonResponse({'error': 'Invalid status'}, status=400)
        if (
            status == Order.Status.CONFIRMED or status == Order.Status.CANCELLED
        ) and order.status != Order.Status.INITIATED:
            return JsonResponse(
                {'error': 'Orders can only be confirmed/cancelled when initiated'}, status=400
            )
        request.status = status

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def validate_pay_data(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)

        card_number = data.get('card-number', None)
        exp_date = data.get('exp-date', None)
        cvc = data.get('cvc', None)
        if not card_number or not exp_date or not cvc:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        request.card_number = card_number
        request.exp_date = exp_date
        request.cvc = cvc
        card_number_regex = r'^\d{4}-\d{4}-\d{4}-\d{4}$'

        exp_date_regex = r'^\d{2}/\d{4}$'

        cvc_regex = r'^\d{3}$'

        if not re.match(card_number_regex, card_number):
            return JsonResponse({'error': 'Invalid card number'}, status=400)

        if not re.match(exp_date_regex, exp_date):
            return JsonResponse({'error': 'Invalid expiration date'}, status=400)

        if not re.match(cvc_regex, cvc):
            return JsonResponse({'error': 'Invalid CVC'}, status=400)

        exp_month, exp_year = map(int, exp_date.split('/'))
        current_year = datetime.now().year
        current_month = datetime.now().month
        if exp_year < current_year or (exp_year == current_year and exp_month < current_month):
            return JsonResponse({'error': 'Card expired'}, status=400)
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def validate_order_pay_exist(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return JsonResponse({'error': 'Order ID is missing'}, status=400)
        try:
            order = Order.objects.get(id=pk)
            request.order = order
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        if order.user != request.user:
            return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
        if order.status != Order.Status.CONFIRMED:
            return JsonResponse({'error': 'Orders can only be paid when confirmed'}, status=400)
        return view_func(request, *args, **kwargs)

    return _wrapped_view
