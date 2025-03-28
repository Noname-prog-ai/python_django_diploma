# from rest_framework import permissions
#
#
# class IsAdmin0rReadOnly(permissions.BasePermission):
#     """Ограничили доступ, можно просматривать, удалять может только админ"""
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return bool(request.user and request.user.is_staff)
#
#
# class IsOwner0rReadOnly(permissions.BasePermission):
#     """Ограничили доступ, можно просматривать, удалять может только автор"""
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.user == request.user
