from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Projet
from .serializers import ProjetSerializer


class ProjetViewSet(viewsets.ModelViewSet):
    queryset = Projet.objects.select_related("id_createur")
    serializer_class = ProjetSerializer
    # MODE TEST - temporary: old security was IsAuthenticated
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "is_anonymous", False):
            return super().get_queryset()
        if user.is_staff or user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(id_createur=user)

    def get_object(self):
        queryset = Projet.objects.all()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]
        obj = queryset.filter(pk=lookup_value).first()
        if obj is None:
            self.kwargs[lookup_url_kwarg] = lookup_value
            return super().get_object()
        if getattr(self.request.user, "is_anonymous", False):
            return obj
        if obj.id_createur != self.request.user and not self.request.user.is_staff:
            self.permission_denied(
                self.request,
                message="Vous n'êtes pas responsable de ce projet.",
                code=None,
            )
        return obj

    def perform_create(self, serializer):
        serializer.save(id_createur=self.request.user)

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        if getattr(request.user, "is_anonymous", False):
            return super().update(request, *args, **kwargs)
        if project.id_createur != request.user and not request.user.is_staff:
            return Response({"detail": "Vous n'êtes pas responsable de ce projet."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        project = self.get_object()
        if getattr(request.user, "is_anonymous", False):
            return super().partial_update(request, *args, **kwargs)
        if project.id_createur != request.user and not request.user.is_staff:
            return Response({"detail": "Vous n'êtes pas responsable de ce projet."}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        if getattr(request.user, "is_anonymous", False):
            return super().destroy(request, *args, **kwargs)
        if project.id_createur != request.user and not request.user.is_staff:
            return Response({"detail": "Vous n'êtes pas responsable de ce projet."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
