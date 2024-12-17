from rest_framework.permissions import BasePermission

class IsAuthor(BasePermission):
    
    def has_permission(self, request, **kwargs):
        return request.user.is_authenticated and request.user.user_type == 'author'
    


class IsReader(BasePermission):

    def has_permission(self, request, **kwargs):
        return request.user.is_authenticated and request.user.user_type == 'reader'
    


class IsAdmin(BasePermission):

    def has_permission(self, request, **kwargs):
        return request.user.is_authenticated and request.user.user_type == 'admin'