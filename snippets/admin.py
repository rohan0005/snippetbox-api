from django.contrib import admin
from .models import Snippet, Comment


# Register your models here.
admin.site.register(Snippet)
admin.site.register(Comment)
