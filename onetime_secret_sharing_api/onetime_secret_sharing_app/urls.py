from django.urls import path
from . import views

urlpatterns = [
  path('secret/', views.post_secret),
  path('secret/<str:uri_random_text>', views.view_secret),
]
