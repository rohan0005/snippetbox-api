from django.rest_framework import serializers
from .models import Snippet, Comment

class SnippetSerializer(serializers.ModelSerializer):
	class Meta:
		model= Snippet
		fields = ['id', 'title', 'code', 'language', 'is_private', 'author', 'created_at']

		def validate_title(self,value):
			if len(value.strip())  <=3:
				raise serializers.ValidationError("Title is too short! It must be at least 4 characters.")
			return value

class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model= Comment
		fields = ['id', 'snippet', 'author', 'content', 'created_at']

		def validate_content(self,value):
			if len(value.strip())  <=3:
				raise serializers.ValidationError("Comment is too short! It must be at least 4 characters.")
			return value

