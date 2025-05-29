from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import CustomUserSerializer, ToDoSerializer
from django.contrib.auth import authenticate
from .models import CustomUser, ToDo
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def user_register(request):
	serializer = CustomUserSerializer(data=request.data)
	if serializer.is_valid():
		user = serializer.save()
		# Generate a token for the user
		token, _ = Token.objects.get_or_create(user=user)
		return Response({"token": token.key}, \
				status=status.HTTP_201_CREATED)
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
def user_todos_list(request):
	if request.method == 'POST':
		serializer = ToDoSerializer(data=request.data)
		if serializer.is_valid():
			# associate the to-do with the authenticated user
			serializer.save(user=request.user)
			return Response(serializer.data, \
					status=status.HTTP_201_CREATED)
		return Response(serializer.errors, \
				status=status.HTTP_400_BAD_REQUEST)	

	elif request.method == 'GET':
		user = request.user  # Get the authenticated user
		todos = ToDo.objects.filter(user=user)  # Filter todos by user
    
		# Get pagination parameters
		page = request.GET.get('page', 1)
		limit = request.GET.get('limit', 10)

		try:
			limit = int(limit)
			if limit <= 0:
				raise ValueError
		except ValueError:
			return Response({"error": "Invalid 'limit' parameter. \
					 Must be a positive integer."},\
					status=status.HTTP_400_BAD_REQUEST)
    
	paginator = Paginator(todos, limit)  # Paginate the todos

	try:
		paginated_todos = paginator.page(page)
	except PageNotAnInteger:
		return Response({"error": "Invalid 'page' parameter. Must be a \
				 positive integer."},\
				status=status.HTTP_400_BAD_REQUEST)
	except EmptyPage:
		return Response({"error": "Page not found."},\
				status=status.HTTP_404_NOT_FOUND)
	
	# Serialize the paginated data
	serializer = ToDoSerializer(paginated_todos.object_list, many=True)
	
	# Return the paginated response
	return Response({
	    "data": serializer.data,
	    "page": paginated_todos.number,
	    "limit": limit,
	    "total": paginator.count
	})

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_todos_detail(request,pk):
	try:
		todo = ToDo.objects.get(pk=pk, user=request.user)
	except ToDo.DoesNotExist:
		return Response({"error": "To Do not found or access denied."},\
				status=status.HTTP_404_NOT_FOUND)
	
	if request.method == 'PUT':
		serializer = ToDoSerializer(todo, data=request.data)
		if serializer.is_valid():
    			serializer.save()
    			return Response(serializer.data)
		return Response(serializer.errors,\
				status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		todo.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

