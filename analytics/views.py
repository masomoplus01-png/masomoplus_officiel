from django.db.models import Count
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from documents.models import Document
from interactions.models import Commentaire, Consultation, Favori, Telechargement


class AnalyticsView(APIView):
    # MODE TEST - temporary: old security was IsAuthenticated
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get(self, request):
        data = {
            "nombre_documents": Document.objects.count(),
            "nombre_telechargements": Telechargement.objects.count(),
            "nombre_consultations": Consultation.objects.count(),
            "nombre_favoris": Favori.objects.count(),
            "nombre_publications": Document.objects.filter(statut="Validé").count(),
        }
        return Response(data, status=status.HTTP_200_OK)
