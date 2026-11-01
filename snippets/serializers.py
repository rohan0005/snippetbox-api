from rest_framework import serializers
from .models import Snippet, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
	    model=User
	    fields = ['id', 'phone_number', 'full_name', ]

class SnippetSerializer(serializers.ModelSerializer):
	author = UserDetailsSerializer(read_only=True)
	class Meta:
		model= Snippet
		fields = '__all__'
		read_only_fields = ['author', 'created_at']

		def validate_title(self,value):
			if len(value.strip())  <=3:
				raise serializers.ValidationError("Title is too short! It must be at least 4 characters.")
			return value

class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model= Comment
		fields = '__all__'
		read_only_fields = ['author', 'created_at']

		def validate_content(self,value):
			if len(value.strip())  <=3:
				raise serializers.ValidationError("Comment is too short! It must be at least 4 characters.")
			return value

