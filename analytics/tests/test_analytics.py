from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from academic.models import Categorie, Département, Faculté, Filière
from analytics.views import AnalyticsView
from interactions.models import Commentaire, Consultation, Favori, Telechargement


class AnalyticsAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            password="StrongPass123!",
            first_name="Test",
            last_name="User",
        )
        self.staff = User.objects.create_user(
            email="staff@example.com",
            password="StrongPass123!",
            first_name="Staff",
            last_name="User",
            is_staff=True,
        )
        self.faculte = Faculté.objects.create(code_faculte="FAC3", nom="Faculté 3")
        self.departement = Département.objects.create(code_departement="DEP3", nom="Dépt 3", faculte=self.faculte)
        self.filiere = Filière.objects.create(code_filiere="FIL3", nom="Filière 3", département=self.departement)
        self.categorie = Categorie.objects.create(code_categorie="CAT3", nom="Catégorie 3")

    def _create_document(self, statut="Validé"):
        from documents.models import Document
        pdf = SimpleUploadedFile("doc.pdf", b"pdf", content_type="application/pdf")
        return Document.objects.create(
            code_document=f"DOC{Document.objects.count() + 1:03d}",
            titre="Document analytics",
            resume="Résumé analytics",
            fichier=pdf,
            annee_publication=2026,
            statut=statut,
            id_categorie=self.categorie,
            id_filiere=self.filiere,
            id_utilisateur=self.user,
        )

    def test_analytics(self):
        document = self._create_document()
        Telechargement.objects.create(code_telechargement="TEL01", id_document=document, id_utilisateur=self.user, adresse_ip="127.0.0.1", appareil="Laptop")
        Consultation.objects.create(id_document=document, id_utilisateur=self.user)
        Favori.objects.create(id_document=document, id_utilisateur=self.user)
        Commentaire.objects.create(id_document=document, id_utilisateur=self.user, contenu="Bon")

        self.client.force_authenticate(user=self.staff)
        response = self.client.get("/api/analytics/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nombre_documents"], 1)
        self.assertEqual(response.data["nombre_telechargements"], 1)
        self.assertEqual(response.data["nombre_consultations"], 1)
        self.assertEqual(response.data["nombre_favoris"], 1)
        self.assertEqual(response.data["nombre_publications"], 1)
