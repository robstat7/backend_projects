from rest_framework import status
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import CustomUser, Tweet, Follower, Like
from .serializers import CustomUserSerializer, TweetSerializer,FollowerSerializer, FollowingSerializer, HomeTweetsSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.db.models import Count

@api_view(['POST'])
def user_signup(request):
  serializer = CustomUserSerializer(data=request.data)
  if serializer.is_valid():
    user = serializer.save()
    # Generate a token for the user                                             
    token, _ = Token.objects.get_or_create(user=user)                           
    return Response({"token": token.key}, status=status.HTTP_201_CREATED) 
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])                                                             
def user_login(request):                                                        
  email = request.data.get('email')                                             
  password = request.data.get('password')                                       
                                                                                
  if not email or not password:                                                 
    return Response({"error": "Email and password are required."},\
        status=status.HTTP_400_BAD_REQUEST)                                     
                                                                                
  # Try to fetch the user by email                                              
  try:                                                                          
    user = CustomUser.objects.get(email=email)                                  
  except CustomUser.DoesNotExist:                                               
    return Response({"error": "Invalid email or password."},\
        status=status.HTTP_401_UNAUTHORIZED)                                    
                                                                                
  # Authenticate the user                                                       
  user = authenticate(username=user.username, password=password)                
                                                                                
  if user is None:                                                              
    return Response({"error": "Invalid email or password."}, \
        status=status.HTTP_401_UNAUTHORIZED)                                    
                                                                                
  # Generate or get an existing token                                           
  token, _ = Token.objects.get_or_create(user=user)                             
                                                                                
  return Response({"token": token.key}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def user_tweets(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        if user_id != request.user.id:
            return Response(
                {"error": "You can't post as another user"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TweetSerializer(
            data=request.data,
            context={
                'request': request,
                'files': request.FILES.getlist('files', [])
            }
        )
        
        if serializer.is_valid():
            tweet = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        tweets = Tweet.objects.filter(tweeter=user)\
                      .prefetch_related('files')\
                      .order_by('-created_on')
        
        tweets_data = []
        for tweet in tweets:
            tweets_data.append({
                "id": tweet.id,
                "tweet": tweet.tweet,
                "created_on": tweet.created_on.strftime('%Y-%m-%d %H:%M:%S'),
                "like_count": Like.objects.filter(tweet=tweet).count(),
                "tweeter_id": user.id,
                "tweeter_username": user.username,
                "files": [
                    {
                        "id": f.id,
                        "url": f.file.url,
                        "uploaded_at": f.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    for f in tweet.files.all()
                ]
            })
        
        return Response({
            "user_id": user.id,
            "username": user.username,
            "tweets_count": tweets.count(),
            "tweets": tweets_data
        }, status=status.HTTP_200_OK)


@api_view(['POST', 'DELETE'])                                             
@permission_classes([IsAuthenticated])
def user_follow(request, user_id):
  try:
    user = CustomUser.objects.get(pk=user_id)
  except CustomUser.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'POST':
    # Check if user is trying to follow themselves
    if request.user.id == user_id:
      return Response(
          {"error": "You cannot follow yourself."},
          status=status.HTTP_400_BAD_REQUEST
      )

    # Check if follow relationship already exists
    if Follower.objects.filter(user=user, follower=request.user).exists():
      return Response(
          {"error": "You are already following this user."},
          status=status.HTTP_400_BAD_REQUEST
      )

    # Create the follow relationship
    try:
      Follower.objects.create(user=user, follower=request.user)
      return Response(
          {"success": f"You are now following {user.username}."},
          status=status.HTTP_201_CREATED
      )
    except Exception as e:
      return Response(
          {"error": str(e)},
          status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )

  elif request.method == 'DELETE':
    # Unfollow the user
    try:
      deleted_count, _ = Follower.objects.filter(user=user, follower=request.user).delete()

      if deleted_count == 0:
        return Response(
            {"error": "You were not following this user."},
            status=status.HTTP_400_BAD_REQUEST
        )

      return Response(
          {"success": f"You have unfollowed {user.username}."},
          status=status.HTTP_200_OK
      )

    except Exception as e:
      return Response(
          {"error": str(e)},
          status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )

# get a user followers
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_followers(request, user_id):
  try:
    user = CustomUser.objects.get(pk=user_id)
  except CustomUser.DoesNotExist:
    return Response({"error": "User not found"},status=status.HTTP_404_NOT_FOUND)

  # Get all follower relationships where this user is being followed
  followers = Follower.objects.filter(user=user).select_related('follower')   

  # Serialize the data
  serializer = FollowerSerializer(followers, many=True)

  return Response(serializer.data, status=status.HTTP_200_OK)

# get a user following
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_following(request, user_id):
  try:
    user = CustomUser.objects.get(pk=user_id)
  except CustomUser.DoesNotExist:
    return Response({"error": "User not found"},status=status.HTTP_404_NOT_FOUND)

  # Get all following relationships where this user is following
  followings = Follower.objects.filter(follower=user).select_related('user')   

  # Serialize the data
  serializer = FollowingSerializer(followings, many=True)

  return Response(serializer.data, status=status.HTTP_200_OK)

# get user home timeline
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_home_timeline(request):
  # Get all users that the current user follows
  following_relationships = Follower.objects.filter(follower=request.user).select_related('user') 
  # Extract the User objects from the relationships
  following_users = [rel.user for rel in following_relationships]

  # Include the current user's own tweets if desired (remove if not needed)
  following_users.append(request.user)

  # Get tweets from all followed users, ordered by creation time (newest first)
  tweets = Tweet.objects.filter(
      tweeter__in=following_users
  ).select_related('tweeter').order_by('-created_on')

  # Serialize the tweets
  serializer = HomeTweetsSerializer(tweets, many=True)

  return Response({
        "following_count": len(following_users) - 1,  # Subtract 1 if including self
        "tweets_count": tweets.count(),
        "tweets": serializer.data
    }, status=status.HTTP_200_OK)


# like or unlike a user tweet
@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def tweet_like(request, tweet_id):
  try:
    tweet = Tweet.objects.get(pk=tweet_id)
  except Tweet.DoesNotExist:
    return Response({"error": "Tweet not found"}, status=status.HTTP_404_NOT_FOUND)

  if request.method == "POST":
    # Like the tweet 
    try:
      Like.objects.create(tweet=tweet, liked_by=request.user)
      return Response(
          {"success": f"You liked tweet id {tweet_id}."},
          status=status.HTTP_201_CREATED
      )
    except Exception as e:
      return Response(
          {"error": str(e)},
          status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )

  elif request.method == "DELETE":
    # Unlike the tweet 
    try:
      deleted_count, _ = Like.objects.filter(tweet=tweet, liked_by=request.user).delete()

      if deleted_count == 0:
        return Response(
            {"error": "You didn't like this tweet in the past."},
            status=status.HTTP_400_BAD_REQUEST
        )

      return Response(
          {"success": f"You have unliked tweet id {tweet_id}."},
          status=status.HTTP_200_OK
      )

    except Exception as e:
      return Response(
          {"error": str(e)},
          status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
