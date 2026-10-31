from django.shortcuts import render
from .serializers import SnippetSerializer, CommentSerializer
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Snippet, Comment
from django.db.models import Q
from .permissions import IsAuthorOrReadOnly


# Create your views here.
class SnippetViewSet(viewsets.ModelViewSet):
    serializer_class = SnippetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly]

    #search filter and ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields   = ['title', 'code', 'language']
    order_fields   = ['created_at', 'title']

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Snippet.objects.filter(is_private=False).order_by('-created_at')
        return Snippet.objects.filter(Q(is_private=False) | Q(author=user)).order_by('-created_at')	

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
    	serializer.save(author=self.request.user)

