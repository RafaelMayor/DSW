from django.urls import path

from . import views

app_name = 'games'

urlpatterns = [
    path('', views.games_list, name='games_list'),
    path('<str:game_slug>/', views.game_details, name='game_details'),
    path('<str:game_slug>/reviews/', views.game_reviews, name='game_reviews'),
    path('reviews/<int:pk>/', views.review_details, name='review_details'),
    path('<str:game_slug>/reviews/add/', views.game_review_add, name='game_review_add'),
]
