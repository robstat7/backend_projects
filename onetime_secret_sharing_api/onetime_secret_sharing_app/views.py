from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import SecretCreateSerializer, SecretViewSerializer 
from .models import Secret
from rest_framework.response import Response
import random
import string

@api_view(['POST'])
def post_secret(request):
  data = request.data.copy()  # Copy the data so we can modify it

  # Generate the uri_random_text and the uri
  length = 12
  random_string = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(length))
  uri_random_text = random_string
  data['uri_random_text'] = uri_random_text 

  uri = '/secret/' + uri_random_text
  data['uri'] = uri

  serializer = SecretCreateSerializer(data=data)
  if serializer.is_valid():                                                   
      serializer.save()                                                         
      return Response(serializer.data, \
          status=status.HTTP_201_CREATED)                                       
      return Response(serializer.errors,\
          status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def view_secret(request, uri_random_text):
  try:                                                                          
    secret = Secret.objects.get(uri_random_text=uri_random_text)                                              
  except Secret.DoesNotExist:                                                     
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  serializer = SecretViewSerializer(secret)                                           

  # store response
  resp = Response(serializer.data)

  # delete secret row
  secret.delete() 

  return resp
