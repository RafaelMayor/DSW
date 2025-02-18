from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('add/', views.order_add, name='order_add'),
    path('<int:pk>/', views.order_details, name='order_details'),
    path('<int:pk>/status/', views.order_status, name='order_status'),
    path('<int:pk>/pay/', views.order_pay, name='order_pay'),
    path('<int:pk>/games/', views.order_games, name='order_games'),
    path('<int:pk>/games/add/', views.order_games_add, name='order_games_add'),
]
