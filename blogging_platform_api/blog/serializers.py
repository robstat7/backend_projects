from rest_framework import serializers
from .models import Post, Category

# description of the class in stackoverflow bookmarked answer in backend folder
# of chrome.
class CategoryRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return Category.objects.get(name=data)


class PostSerializer(serializers.ModelSerializer):
	# categories = serializers.StringRelatedField(many=True)

	# To serialize a queryset or list of objects instead of a single
	# object instance, you should pass the many=True.
	categories = CategoryRelatedField(
			queryset=Category.objects.all(),
			many=True
			)

	class Meta:
		model = Post
		fields = ['id', 'title', 'content', 'created_on',\
			  'last_modified', 'categories']
