from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from academic.models import Categorie, Département, Faculté, Filière
from interactions.models import Commentaire, Consultation, Favori, Telechargement


class InteractionsAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            password="StrongPass123!",
            first_name="Test",
            last_name="User",
        )
        self.other = User.objects.create_user(
            email="other@example.com",
            password="StrongPass123!",
            first_name="Other",
            last_name="User",
        )
        self.faculte = Faculté.objects.create(code_faculte="FAC2", nom="Faculté 2")
        self.departement = Département.objects.create(code_departement="DEP2", nom="Dépt 2", faculte=self.faculte)
        self.filiere = Filière.objects.create(code_filiere="FIL2", nom="Sciences", département=self.departement)
        self.categorie = Categorie.objects.create(code_categorie="CAT2", nom="Article")

    def _create_document(self):
        from documents.models import Document
        pdf = SimpleUploadedFile("doc.pdf", b"pdf", content_type="application/pdf")
        return Document.objects.create(
            code_document=f"DOC{Document.objects.count() + 1:03d}",
            titre="Doc",
            resume="Résumé",
            fichier=pdf,
            annee_publication=2026,
            statut="Validé",
            id_categorie=self.categorie,
            id_filiere=self.filiere,
            id_utilisateur=self.user,
        )

    def test_download(self):
        document = self._create_document()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/interactions/telechargements/",
            {"id_document": document.id_document, "code_telechargement": "TEL001", "adresse_ip": "127.0.0.1", "appareil": "Laptop"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Telechargement.objects.count(), 1)

    def test_consultation(self):
        document = self._create_document()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/interactions/consultations/",
            {"id_document": document.id_document},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Consultation.objects.count(), 1)

    def test_favorite(self):
        document = self._create_document()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/interactions/favoris/",
            {"id_document": document.id_document},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Favori.objects.count(), 1)

        delete_response = self.client.delete(f"/api/interactions/favoris/{Favori.objects.get(id_utilisateur=self.user, id_document=document).id_favori}/")
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_comment(self):
        document = self._create_document()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/interactions/commentaires/",
            {"id_document": document.id_document, "contenu": "Très bon document"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Commentaire.objects.count(), 1)

        edit = self.client.patch(
            f"/api/interactions/commentaires/{Commentaire.objects.get(id_utilisateur=self.user).id_commentaire}/",
            {"contenu": "Modification"},
            format="json",
        )
        self.assertEqual(edit.status_code, status.HTTP_200_OK)

    def test_comment_permission(self):
        document = self._create_document()
        comment = Commentaire.objects.create(id_document=document, id_utilisateur=self.user, contenu="texte")
        self.client.force_authenticate(user=self.other)
        response = self.client.patch(f"/api/interactions/commentaires/{comment.id_commentaire}/", {"contenu": "hack"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
