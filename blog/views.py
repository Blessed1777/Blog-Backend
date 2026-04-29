from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from . models import Post, Comment, User
from . serializers import PostSerializer, CommentSerializer, RegisterSerializer
from rest_framework import viewsets
from .permissions import IsAuthorOrReadOnly, IsCommentOwnerOrPostAuthor
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from . filters import PostFilter
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import PermissionDenied




class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in")
        serializer.save(author=self.request.user)
        
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PostFilter
    search_fields = ['title', 'content', 'author__username']
    ordering_fields = ['created_at']

    @extend_schema(request=None)
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if post.likes.filter(id=user.id).exists():
            return Response({
                "message": "You already liked this post"
            }, status=400)

        post.likes.add(user)
        post.dislikes.remove(user)

        return Response({
            "message": "Post liked",
            "likes": post.likes.count(),
           "dislikes": post.dislikes.count()
        })

    @extend_schema(request=None)
    @action(detail=True, methods=['post'])
    def dislike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if post.dislikes.filter(id=user.id).exists():
           return Response({
               "message": "You already disliked this post"
               }, status=400)

        post.dislikes.add(user)
        post.likes.remove(user)

        return Response({
            "message": "Post disliked",
            "likes": post.likes.count(),
            "dislikes": post.dislikes.count()
            })



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentOwnerOrPostAuthor]

    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

