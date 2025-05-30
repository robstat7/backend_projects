from django.db import models
from django.contrib.auth.models import AbstractUser                             
from django.core.validators import FileExtensionValidator
                                                                                
class CustomUser(AbstractUser):                                                 
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  email = models.EmailField(max_length=400, unique=True)                        
  username = models.CharField(max_length=300, unique=True)
  password = models.CharField(max_length=300)

class Tweet(models.Model):
  tweet = models.CharField(max_length=280)
  created_on = models.DateTimeField(auto_now_add=True)
  tweeter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Follower(models.Model):
  followed_on = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers')
  follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')

  class Meta:
    unique_together = ('user', 'follower')  # Critical for preventing duplicate follows


class Like(models.Model):
  liked_on = models.DateTimeField(auto_now_add=True)
  tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE) 
  liked_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class TweetFile(models.Model):
  tweet = models.ForeignKey(
      'Tweet', 
      on_delete=models.CASCADE,
      related_name='files'
  )
  file = models.FileField(
      upload_to='tweet_files/%Y/%m/%d/',
      validators=[
          FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])
      ]
  )
  uploaded_at = models.DateTimeField(auto_now_add=True)
  file_type = models.CharField(max_length=10, blank=True)
  
  class Meta:
      verbose_name = 'Tweet File'
      verbose_name_plural = 'Tweet Files'
      ordering = ['-uploaded_at']
  
  def save(self, *args, **kwargs):
      # Auto-detect file type from extension
      if not self.file_type and self.file:
          ext = self.file.name.split('.')[-1].lower()
          if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
              self.file_type = 'image'
      super().save(*args, **kwargs)
  
  def __str__(self):
      return f"File for Tweet #{self.tweet.id}"
