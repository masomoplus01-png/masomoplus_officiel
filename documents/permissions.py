from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrStaffOrReadOnly(BasePermission):
    message = "Vous n'êtes pas autorisé à modifier ce document."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user and (request.user.is_staff or request.user.is_superuser):
            return True
        return obj.id_utilisateur_id == getattr(request.user, "id", None)
