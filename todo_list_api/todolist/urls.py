from django.urls import path
from . import views

urlpatterns = [
        path('register/', views.user_register),
        path('login/', views.user_login),
        path('todos/', views.user_todos_list),
        path('todos/<int:pk>', views.user_todos_detail),
]
