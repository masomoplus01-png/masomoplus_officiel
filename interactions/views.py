from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from documents.models import Document
from .models import Commentaire, Consultation, Favori, Telechargement
from .serializers import (
    CommentaireSerializer,
    ConsultationSerializer,
    FavoriSerializer,
    TelechargementSerializer,
)


class TelechargementViewSet(viewsets.ModelViewSet):
    queryset = Telechargement.objects.select_related("id_document", "id_utilisateur")
    serializer_class = TelechargementSerializer
    # MODE TEST - temporary: old security was IsAuthenticated
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(id_utilisateur=self.request.user)


class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.select_related("id_document", "id_utilisateur")
    serializer_class = ConsultationSerializer
    # MODE TEST - temporary: old security was IsAuthenticated
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(id_utilisateur=self.request.user)


class FavoriViewSet(viewsets.ModelViewSet):
    queryset = Favori.objects.select_related("id_document", "id_utilisateur")
    serializer_class = FavoriSerializer
    # MODE TEST - temporary: old security was IsAuthenticated
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get_queryset(self):
        return super().get_queryset().filter(id_utilisateur=self.request.user)

    def perform_create(self, serializer):
        serializer.save(id_utilisateur=self.request.user)


class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.select_related("id_document", "id_utilisateur")
    serializer_class = CommentaireSerializer
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

    def get_object(self):
        queryset = Commentaire.objects.all()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]
        obj = queryset.filter(pk=lookup_value).first()
        if obj is None:
            self.kwargs[lookup_url_kwarg] = lookup_value
            return super().get_object()
        if getattr(self.request.user, "is_anonymous", False):
            return obj
        if obj.id_utilisateur != self.request.user and not self.request.user.is_staff:
            self.permission_denied(
                self.request,
                message="Vous ne pouvez modifier que votre propre commentaire.",
                code=None,
            )
        return obj

    def perform_create(self, serializer):
        if getattr(self.request.user, "is_anonymous", False):
            serializer.save()
            return
        serializer.save(id_utilisateur=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if getattr(request.user, "is_anonymous", False):
            return super().update(request, *args, **kwargs)
        if instance.id_utilisateur != request.user and not request.user.is_staff:
            return Response({"detail": "Vous ne pouvez modifier que votre propre commentaire."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if getattr(request.user, "is_anonymous", False):
            return super().destroy(request, *args, **kwargs)
        if instance.id_utilisateur != request.user and not request.user.is_staff:
            return Response({"detail": "Vous ne pouvez supprimer que votre propre commentaire."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
