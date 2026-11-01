from django.shortcuts import render
from .serializers import SnippetSerializer, CommentSerializer
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Snippet, Comment
from django.db.models import Q
from .permissions import IsAuthorOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response


# Create your views here.
class SnippetViewSet(viewsets.ModelViewSet):
    serializer_class = SnippetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly]

    #search filter and ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields   = ['title', 'code', 'language']
    ordering_fields   = ['created_at', 'title']

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Snippet.objects.filter(is_private=False).order_by('-created_at')
        return Snippet.objects.filter(Q(is_private=False) | Q(author=user)).order_by('-created_at')	

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def my_vault(self,request):
        my_snippets = Snippet.objects.filter(author=self.request.user).order_by('-created_at')
        
        #paginate 
        page = self.paginate_queryset(my_snippets)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(my_snippets,many=True)
        return Response({
            "response": True,
            "result": serializer.data,
            "msg": "My Snippet fetched!"
        })


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
    	serializer.save(author=self.request.user)

