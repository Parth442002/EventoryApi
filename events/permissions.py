from rest_framework import permissions


class isCreator(permissions.BasePermission):
    """
    A base class from which all permission classes should inherit.
    """
    edit_methods = ("PUT", "PATCH", "DELETE")

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """

        if request.user.is_authenticated and request.user.is_verified:
            return True
        if request.user.is_authenticated and request.user.is_verified == False:
            if request.method in ["GET"]:
                return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.user.is_superuser:
            return True

        if request.user.is_authenticated and request.method == "GET":
            return True

        if request.user.is_verified:
            return False

        if request.user.is_staff and request.method not in self.edit_methods:
            return True

        # Checking if the signed in user is the event Creator or not.
        if obj.creator.id == request.user.id:
            return True

        return False
