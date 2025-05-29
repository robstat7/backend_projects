from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from django.db.models import Q

@api_view(['GET', 'POST'])
def post_list(request):
	if request.method == 'GET':
		posts = Post.objects.all()
		term = request.GET.get('term', None)
		if term:
			queryset = posts.filter(
            			Q(title__icontains=term) |
            			Q(content__icontains=term) |
            			Q(categories__name__icontains=term)
        			).distinct()
				# Use `distinct` to avoid duplicate posts due to 
		      		# category matches.			
			serializer = PostSerializer(queryset, many=True)
			return Response(serializer.data)
		else:
			serializer = PostSerializer(posts, many=True)
			return Response(serializer.data)

	elif request.method == 'POST':
		serializer = PostSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, \
					status=status.HTTP_201_CREATED)
		return Response(serializer.errors,\
				status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):
	try:
		post = Post.objects.get(pk=pk)
	except Post.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = PostSerializer(post)
		return Response(serializer.data)

	elif request.method == 'PUT':
		serializer = PostSerializer(post, data=request.data)
		if serializer.is_valid():
    			serializer.save()
    			return Response(serializer.data)
		return Response(serializer.errors,\
				status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		post.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
