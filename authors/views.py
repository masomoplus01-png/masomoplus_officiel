from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Auteur, DocumentAuteur
from .serializers import AuteurSerializer, DocumentAuteurSerializer


class AuteurViewSet(viewsets.ModelViewSet):
    queryset = Auteur.objects.all()
    serializer_class = AuteurSerializer


class DocumentAuteurViewSet(viewsets.ModelViewSet):
    queryset = DocumentAuteur.objects.all()
    serializer_class = DocumentAuteurSerializer

    @action(detail=False, methods=["post"], url_path="associate")
    def add_author_to_document(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["patch"], url_path="update-role")
    def update_author_role(self, request, pk=None):
        instance = self.get_object()
        role = request.data.get("role_auteur")
        if role not in dict(DocumentAuteur.ROLE_CHOICES):
            return Response({"detail": "Rôle invalide."}, status=status.HTTP_400_BAD_REQUEST)
        instance.role_auteur = role
        instance.save()
        return Response(self.get_serializer(instance).data)

    @action(detail=True, methods=["delete"], url_path="remove")
    def remove_author(self, request, pk=None):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
