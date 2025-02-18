import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from categories.models import Category
from platforms.models import Platform
from shared.decorators import method_required, token_required
from shared.utils import custom_404

from .decorators import validate_review_data
from .models import Game, Review
from .serializers import GamesSerializer, ReviewsSerializer


@csrf_exempt
@method_required('GET')
def games_list(request):
    platform = request.GET.get('platform', None)
    category = request.GET.get('category', None)

    games = Game.objects.all()

    if platform:
        platform_instance = Platform.objects.get(slug=platform)
        games = games.filter(platforms=platform_instance)
    if category:
        category_instance = Category.objects.get(slug=category)
        games = games.filter(category=category_instance)

    serializes_games = GamesSerializer(games, request=request)

    return JsonResponse(serializes_games.serialize(), safe=False)


@method_required('GET')
def game_details(request, game_slug):
    try:
        game = GamesSerializer(Game.objects.get(slug=game_slug), request=request)
    except Game.DoesNotExist:
        return custom_404('Game not found')
    return JsonResponse(game.serialize(), safe=False)


@method_required('GET')
def game_reviews(request, game_slug):
    try:
        game = Game.objects.get(slug=game_slug)
    except Game.DoesNotExist:
        return custom_404('Game not found')

    reviews = ReviewsSerializer(game.game_reviews.all(), request=request)
    return reviews.json_response()


@method_required('GET')
def review_details(request, pk):
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return custom_404('Review not found')

    reviews = ReviewsSerializer(review, request=request)
    return reviews.json_response()


@csrf_exempt
@method_required('POST')
@validate_review_data
@token_required
def game_review_add(request, game_slug):
    try:
        data = json.loads(request.body)
        rating = data['rating']
        comment = data['comment']
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    try:
        game = Game.objects.get(slug=game_slug)
    except Game.DoesNotExist:
        return custom_404('Game not found')

    new_review = Review.objects.create(
        rating=rating, comment=comment, game=game, author=request.user
    )

    return JsonResponse({'id': new_review.pk}, status=200)
