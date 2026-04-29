from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, RegisterViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('comments', CommentViewSet, basename='comments')
router.register('register', RegisterViewSet, basename='register')


urlpatterns = [
    path('', include(router.urls)),
]
