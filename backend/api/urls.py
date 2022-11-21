from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('auth/login', views.login_handler),
    path('auth/callback/<str:sessionid>', views.callback_handler)
]