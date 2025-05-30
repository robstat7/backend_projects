from rest_framework import serializers
from django.contrib.auth.hashers import make_password                           
from django.contrib.auth import get_user_model                                  
from django.contrib.auth.models import User                                     
from .models import Tweet, Follower, TweetFile, Like

User = get_user_model()  # Get the custom user model

class CustomUserSerializer(serializers.ModelSerializer):                        
  class Meta:                                                                   
    model = User                                                    
    fields = ['first_name', 'last_name', 'email', 'username', 'password']
                                                                                
  def create(self, validated_data):                                             
    # Hash the password before saving the user                            
    validated_data['password'] = make_password(validated_data['password'])                
    return super().create(validated_data)

class TweetSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    files = serializers.SerializerMethodField()
    
    class Meta:
        model = Tweet
        fields = ['id', 'tweet', 'created_on', 'tweeter', 'like_count', 'files']
        read_only_fields = ['id', 'created_on', 'tweeter', 'like_count', 'files']

    def get_like_count(self, obj):
        return Like.objects.filter(tweet=obj).count()

    def get_files(self, obj):
        return [
            {
                'id': f.id,
                'url': f.file.url,
                'uploaded_at': f.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            for f in obj.files.all()
        ]

    def create(self, validated_data):
        files = self.context.get('files', [])
        tweet = Tweet.objects.create(
            tweeter=self.context['request'].user,
            **validated_data
        )
        
        for file in files:
            TweetFile.objects.create(tweet=tweet, file=file)
            
        return tweet

class FollowerSerializer(serializers.ModelSerializer):
    follower_id = serializers.ReadOnlyField(source='follower.id')
    follower_username = serializers.ReadOnlyField(source='follower.username')
    followed_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Follower
        fields = ['follower_id', 'follower_username', 'followed_on']

class FollowingSerializer(serializers.ModelSerializer):
    following_id = serializers.ReadOnlyField(source='user.id')
    following_username = serializers.ReadOnlyField(source='user.username')
    followed_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Follower
        fields = ['following_id', 'following_username', 'followed_on']


class HomeTweetsSerializer(serializers.ModelSerializer):
    tweeter_id = serializers.ReadOnlyField(source='tweeter.id')
    tweeter_username = serializers.ReadOnlyField(source='tweeter.username')
    created_on = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Tweet
        fields = [
            'id',
            'tweet',
            'created_on',
            'tweeter_id',
            'tweeter_username'
        ]
