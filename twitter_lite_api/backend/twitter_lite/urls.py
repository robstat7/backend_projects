from django.urls import path                                                    
from . import views                                                             
from django.conf import settings
from django.conf.urls.static import static
                                                                                
urlpatterns = [                                                                 
   path('api/users/signup/', views.user_signup),                                              
   path('api/users/login/', views.user_login),

   path('api/users/<int:user_id>/tweets/', views.user_tweets), # Get a user's tweets or post a new one

   path('api/users/<int:user_id>/follow/', views.user_follow), # follow or unfollow a user (using POST and DELETE methods)

   path('api/users/<int:user_id>/followers/', views.user_followers), # Get a user's followers
   path('api/users/<int:user_id>/following/', views.user_following), # Get a user's following list

   path('api/users/home-timeline/', views.user_home_timeline), # Get the authenticated user's home timeline

   path('api/tweets/<int:tweet_id>/like/', views.tweet_like),  # Like or unlike a tweet by the authenticated user
]

if settings.DEBUG:  # Only in development mode!
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
