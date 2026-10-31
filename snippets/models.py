from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class Snippet(models.Model):
	title = models.CharField(max_length=20)
	code = models.TextField()
	language = models.CharField(max_length=20)
	is_private= models.BooleanField(default=False)
	author= models.ForeignKey(settings
		.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="snippet")
	created_at = models.DateTimeField(auto_now_add=True
		)

	def __str__(self):
		return self.title

class Comment(models.Model):
	snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE,
		related_name="comment")
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
	content = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.snippet.title
