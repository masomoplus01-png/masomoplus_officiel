from django.db.models import Q
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Document
from .permissions import IsOwnerOrStaffOrReadOnly
from .serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.select_related("id_categorie", "id_filiere", "id_utilisateur")
    serializer_class = DocumentSerializer
    # MODE TEST - temporary: old security was IsAuthenticated + IsOwnerOrStaffOrReadOnly
    # permission_classes = [IsAuthenticated, IsOwnerOrStaffOrReadOnly]
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["titre", "resume", "mots_cles"]
    ordering_fields = ["annee_publication", "date_depot", "statut"]

    def get_queryset(self):
        queryset = super().get_queryset()

        categorie = self.request.query_params.get("categorie")
        filiere = self.request.query_params.get("filiere")
        annee = self.request.query_params.get("annee")
        statut = self.request.query_params.get("statut")
        auteur = self.request.query_params.get("auteur")

        if categorie:
            queryset = queryset.filter(id_categorie_id=categorie)
        if filiere:
            queryset = queryset.filter(id_filiere_id=filiere)
        if annee:
            queryset = queryset.filter(annee_publication=annee)
        if statut:
            queryset = queryset.filter(statut=statut)
        if auteur:
            queryset = queryset.filter(document_auteurs__id_auteur_id=auteur).distinct()

        return queryset

    def perform_create(self, serializer):
        serializer.save(id_utilisateur=self.request.user)

    @action(detail=False, methods=["get"], url_path="search")
    def search_documents(self, request):
        query = request.query_params.get("q", "")
        queryset = self.get_queryset()
        if query:
            queryset = queryset.filter(
                Q(titre__icontains=query)
                | Q(resume__icontains=query)
                | Q(mots_cles__icontains=query)
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], url_path="status")
    def update_status(self, request, pk=None):
        document = self.get_object()
        if not (request.user.is_staff or request.user.is_superuser or document.id_utilisateur == request.user):
            return Response({"detail": "Vous n'êtes pas autorisé à modifier ce statut."}, status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get("statut")
        if new_status not in dict(Document.STATUS_CHOICES):
            return Response({"detail": "Statut invalide."}, status=status.HTTP_400_BAD_REQUEST)

        document.statut = new_status
        document.save()
        return Response(self.get_serializer(document).data)
