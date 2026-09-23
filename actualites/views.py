from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Actualite
from .serializers import ActualiteSerializer


class ActualiteViewSet(viewsets.ModelViewSet):
    queryset = Actualite.objects.select_related("id_auteur")
    serializer_class = ActualiteSerializer
    # MODE TEST - temporary: old security was IsAuthenticated
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "is_anonymous", False):
            return super().get_queryset()
        if user.is_staff or user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(id_auteur=user)

    def get_object(self):
        queryset = Actualite.objects.all()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]
        obj = queryset.filter(pk=lookup_value).first()
        if obj is None:
            self.kwargs[lookup_url_kwarg] = lookup_value
            return super().get_object()
        if getattr(self.request.user, "is_anonymous", False):
            return obj
        if obj.id_auteur != self.request.user and not self.request.user.is_staff:
            self.permission_denied(
                self.request,
                message="Vous ne pouvez modifier que vos propres actualités.",
                code=None,
            )
        return obj

    def perform_create(self, serializer):
        if getattr(self.request.user, "is_anonymous", False):
            serializer.save()
            return
        serializer.save(id_auteur=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if getattr(request.user, "is_anonymous", False):
            return super().update(request, *args, **kwargs)
        if instance.id_auteur != request.user and not request.user.is_staff:
            return Response({"detail": "Vous ne pouvez modifier que vos propres actualités."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if getattr(request.user, "is_anonymous", False):
            return super().partial_update(request, *args, **kwargs)
        if instance.id_auteur != request.user and not request.user.is_staff:
            return Response({"detail": "Vous ne pouvez modifier que vos propres actualités."}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if getattr(request.user, "is_anonymous", False):
            return super().destroy(request, *args, **kwargs)
        if instance.id_auteur != request.user and not request.user.is_staff:
            return Response({"detail": "Vous ne pouvez supprimer que vos propres actualités."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
