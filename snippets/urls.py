from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SnippetViewSet, CommentViewSet
router = DefaultRouter()

router.register(r'snippets',SnippetViewSet, basename='snippet')
router.register(r'comments',CommentViewSet, basename='comments')

urlpatterns = [
	
	path('', include(router.urls)),

]