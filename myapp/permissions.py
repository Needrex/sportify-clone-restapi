from rest_framework.permissions import BasePermission

class IsNotAuthenticated(BasePermission):
    """
    Izinkan akses hanya untuk user yang BELUM terautentikasi.
    """

    def has_permission(self, request, view):
        return not request.user or not request.user.is_authenticated
