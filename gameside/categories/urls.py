from django.urls import path

from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.categories_list, name='categories_list'),
    path('<str:slug>/', views.category_details, name='category_details'),
]
