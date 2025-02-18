from django.urls import path

from . import views

app_name = 'platform'

urlpatterns = [
    path('', views.platorms_list, name='platforms_list'),
    path('<str:slug>/', views.platform_details, name='platform_details'),
]
