from rest_framework import serializers
from .models import Secret

class SecretCreateSerializer(serializers.ModelSerializer):
  uri_random_text = serializers.CharField(write_only=True)
  text = serializers.CharField(write_only=True)

  class Meta:                                                                   
    model = Secret
    fields = ['uri', 'uri_random_text', 'text']

class SecretViewSerializer(serializers.ModelSerializer):
  class Meta:                                                                   
    model = Secret
    fields = ['text']
