from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('auth/status', views.login_status),
    path('auth/login', views.login_handler),
    path('auth/logout', views.logout_handler),
    path('auth/callback/<str:sessionid>', views.callback_handler),
    path('auth/user', views.current_user),
    path('user/update', views.update_user)
    # path('schedule/<int:id>', views.schedule)
]