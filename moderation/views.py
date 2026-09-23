from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import Validation
from .serializers import ValidationSerializer


class ValidationViewSet(viewsets.ModelViewSet):
    queryset = Validation.objects.select_related("id_document", "id_utilisateur")
    serializer_class = ValidationSerializer
    # MODE TEST - temporary: old security was IsAuthenticated + IsAdminUser
    # permission_classes = [IsAuthenticated, IsAdminUser]
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "is_anonymous", False):
            return super().get_queryset()
        if user.is_staff or user.is_superuser:
            return super().get_queryset()
        return Validation.objects.filter(id_utilisateur=user)

    @action(detail=False, methods=["get"], url_path="document")
    def by_document(self, request):
        document_id = request.query_params.get("document_id")
        if not document_id:
            return Response({"detail": "document_id requis."}, status=status.HTTP_400_BAD_REQUEST)

        qs = Validation.objects.filter(id_document_id=document_id)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="accept")
    def accept_validation(self, request, pk=None):
        validation = self.get_object()
        if not (request.user.is_staff or request.user.is_superuser):
            return Response({"detail": "Accès interdit."}, status=status.HTTP_403_FORBIDDEN)
        validation.decision = "Accepté"
        validation.commentaire = request.data.get("commentaire", validation.commentaire)
        validation.save()
        validation.id_document.statut = "Accepté"
        validation.id_document.save(update_fields=["statut"])
        return Response(self.get_serializer(validation).data)

    @action(detail=True, methods=["post"], url_path="reject")
    def reject_validation(self, request, pk=None):
        validation = self.get_object()
        if not (request.user.is_staff or request.user.is_superuser):
            return Response({"detail": "Accès interdit."}, status=status.HTTP_403_FORBIDDEN)
        validation.decision = "Rejeté"
        validation.commentaire = request.data.get("commentaire", validation.commentaire)
        validation.save()
        validation.id_document.statut = "Rejeté"
        validation.id_document.save(update_fields=["statut"])
        return Response(self.get_serializer(validation).data)

    @action(detail=True, methods=["post"], url_path="archive")
    def archive_validation(self, request, pk=None):
        validation = self.get_object()
        if not (request.user.is_staff or request.user.is_superuser):
            return Response({"detail": "Accès interdit."}, status=status.HTTP_403_FORBIDDEN)
        validation.decision = "Archivé"
        validation.commentaire = request.data.get("commentaire", validation.commentaire)
        validation.save()
        validation.id_document.statut = "Archivé"
        validation.id_document.save(update_fields=["statut"])
        return Response(self.get_serializer(validation).data)
