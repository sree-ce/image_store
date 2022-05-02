from rest_framework.permissions import BasePermission

class IsAuthenticatedCustomer(BasePermission):

    def has_permission(self, request, view):

        try:
            return request.user.is_active
        except:
            return False