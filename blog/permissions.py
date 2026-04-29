# permissions.py
from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the author to edit/delete the object.
    """
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS are GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only allow author to edit/delete
        return obj.author == request.user



class IsCommentOwnerOrPostAuthor(permissions.BasePermission):
    """
    Allow comment owner to edit/delete, or post author to delete any comment on their post.
    """
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS are GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow comment author to edit/delete
        if obj.author == request.user:
            return True
        # Allow post author to delete comments on their post
        if request.method == 'DELETE' and obj.post.author == request.user:
            return True
        return False
