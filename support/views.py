from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Support
from .serializers import SupportSerializer


class SupportViewSet(viewsets.ModelViewSet):
    queryset = Support.objects.select_related("id_utilisateur")
    serializer_class = SupportSerializer
    # MODE TEST - temporary: old security was IsAuthenticated
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "is_anonymous", False):
            return super().get_queryset()
        if user.is_staff or user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(id_utilisateur=user)

    def perform_create(self, serializer):
        serializer.save(id_utilisateur=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if getattr(request.user, "is_anonymous", False):
            return super().update(request, *args, **kwargs)
        if instance.id_utilisateur != request.user and not request.user.is_staff:
            return Response({"detail": "Vous ne pouvez modifier que vos propres tickets."}, status=status.HTTP_403_FORBIDDEN)
        if "date_resolution" in request.data and request.data["date_resolution"]:
            instance.date_resolution = timezone.now()
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if getattr(request.user, "is_anonymous", False):
            return super().partial_update(request, *args, **kwargs)
        if instance.id_utilisateur != request.user and not request.user.is_staff:
            return Response({"detail": "Vous ne pouvez modifier que vos propres tickets."}, status=status.HTTP_403_FORBIDDEN)
        if request.data.get("statut") == "Résolu" and not instance.date_resolution:
            instance.date_resolution = timezone.now()
            instance.save(update_fields=["date_resolution"])
        return super().partial_update(request, *args, **kwargs)
