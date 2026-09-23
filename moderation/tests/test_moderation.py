from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from academic.models import Categorie, Département, Faculté, Filière
from moderation.models import Validation


class ModerationAPITests(APITestCase):
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
        self.faculte = Faculté.objects.create(code_faculte="FAC1", nom="Faculté")
        self.departement = Département.objects.create(code_departement="DEP1", nom="Dépt", faculte=self.faculte)
        self.filiere = Filière.objects.create(code_filiere="FIL1", nom="Informatique", département=self.departement)
        self.categorie = Categorie.objects.create(code_categorie="CAT1", nom="Mémoire")

    def _create_document(self, statut="Brouillon"):
        pdf = SimpleUploadedFile("doc.pdf", b"pdf-content", content_type="application/pdf")
        from documents.models import Document
        return Document.objects.create(
            code_document=f"DOC{Document.objects.count() + 1:03d}",
            titre="Titre",
            resume="Résumé",
            fichier=pdf,
            annee_publication=2026,
            statut=statut,
            id_categorie=self.categorie,
            id_filiere=self.filiere,
            id_utilisateur=self.user,
        )

    def test_validation(self):
        document = self._create_document(statut="En attente")
        self.client.force_authenticate(user=self.staff)
        response = self.client.post(
            "/api/moderation/",
            {"code_validation": "VAL001", "id_document": document.id_document, "decision": "Accepté", "commentaire": "OK"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Validation.objects.count(), 1)

    def test_accept(self):
        document = self._create_document(statut="En attente")
        self.client.force_authenticate(user=self.staff)
        response = self.client.post(f"/api/moderation/{Validation.objects.create(code_validation='VAL002', id_document=document, id_utilisateur=self.staff, decision='En attente').id_validation}/accept/", {"commentaire": "Bonne pièce"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["decision"], "Accepté")

    def test_reject(self):
        document = self._create_document(statut="En attente")
        self.client.force_authenticate(user=self.staff)
        validation = Validation.objects.create(code_validation='VAL003', id_document=document, id_utilisateur=self.staff, decision='En attente')
        response = self.client.post(f"/api/moderation/{validation.id_validation}/reject/", {"commentaire": "Mauvais format"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["decision"], "Rejeté")

    def test_archive(self):
        document = self._create_document(statut="Accepté")
        self.client.force_authenticate(user=self.staff)
        validation = Validation.objects.create(code_validation='VAL004', id_document=document, id_utilisateur=self.staff, decision='Accepté')
        response = self.client.post(f"/api/moderation/{validation.id_validation}/archive/", {"commentaire": "Archivé"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["decision"], "Archivé")

    def test_invalid_workflow(self):
        document = self._create_document(statut="Brouillon")
        self.client.force_authenticate(user=self.staff)
        response = self.client.post(
            "/api/moderation/",
            {"code_validation": "VAL005", "id_document": document.id_document, "decision": "Accepté", "commentaire": "bad"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_permissions(self):
        document = self._create_document(statut="En attente")
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/moderation/",
            {"code_validation": "VAL006", "id_document": document.id_document, "decision": "Accepté", "commentaire": "bad"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
