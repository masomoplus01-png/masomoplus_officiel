import os
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from academic.models import Categorie, Département, Faculté, Filière
from documents.models import Document


class DocumentAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            password="StrongPass123!",
            first_name="Test",
            last_name="User",
        )
        self.staff = User.objects.create_user(
            email="admin@example.com",
            password="StrongPass123!",
            first_name="Admin",
            last_name="User",
            is_staff=True,
        )
        self.categorie = Categorie.objects.create(code_categorie="CAT1", nom="Mémoire")
        self.faculte = Faculté.objects.create(code_faculte="FAC1", nom="Faculté des Sciences")
        self.departement = Département.objects.create(
            code_departement="DEP1",
            nom="Département Informatique",
            faculte=self.faculte,
        )
        self.filiere = Filière.objects.create(
            code_filiere="FIL1",
            nom="Informatique",
            département=self.departement,
        )

    def test_create_document(self):
        pdf = SimpleUploadedFile("document.pdf", b"pdf-content", content_type="application/pdf")

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/documents/",
            {
                "code_document": "DOC001",
                "titre": "Mon document",
                "resume": "Résumé scientifique",
                "mots_cles": "django, api",
                "fichier": pdf,
                "annee_publication": 2026,
                "langue": "Français",
                "nombre_pages": 30,
                "statut": "Brouillon",
                "id_categorie": self.categorie.id,
                "id_filiere": self.filiere.id,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Document.objects.count(), 1)
        self.assertEqual(response.data["code_document"], "DOC001")

    def test_list_and_retrieve_document(self):
        pdf = SimpleUploadedFile("document.pdf", b"pdf-content", content_type="application/pdf")
        Document.objects.create(
            code_document="DOC002",
            titre="Doc 2",
            resume="Résumé 2",
            mots_cles="test",
            fichier=pdf,
            annee_publication=2025,
            langue="Français",
            nombre_pages=10,
            statut="Validé",
            id_categorie=self.categorie,
            id_filiere=self.filiere,
            id_utilisateur=self.user,
        )

        self.client.force_authenticate(user=self.user)
        list_response = self.client.get("/api/documents/")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(list_response.data), 0)

        detail_response = self.client.get("/api/documents/1/")
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)

    def test_document_update_and_delete(self):
        pdf = SimpleUploadedFile("document.pdf", b"pdf-content", content_type="application/pdf")
        doc = Document.objects.create(
            code_document="DOC003",
            titre="Ancien titre",
            resume="Ancien résumé",
            fichier=pdf,
            annee_publication=2024,
            statut="Brouillon",
            id_categorie=self.categorie,
            id_filiere=self.filiere,
            id_utilisateur=self.user,
        )

        self.client.force_authenticate(user=self.user)
        patch_response = self.client.patch(
            f"/api/documents/{doc.id_document}/",
            {"titre": "Nouveau titre", "statut": "Attente"},
            format="json",
        )
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.data["titre"], "Nouveau titre")

        delete_response = self.client.delete(f"/api/documents/{doc.id_document}/")
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_document_filtering_and_search(self):
        pdf = SimpleUploadedFile("document.pdf", b"pdf-content", content_type="application/pdf")
        Document.objects.create(
            code_document="DOC004",
            titre="Recherche sur Django",
            resume="Résumé de test",
            mots_cles="django rest framework",
            fichier=pdf,
            annee_publication=2023,
            statut="Validé",
            id_categorie=self.categorie,
            id_filiere=self.filiere,
            id_utilisateur=self.user,
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/documents/?search=Django&statut=Validé&categorie=%s&filiere=%s&annee=2023" % (self.categorie.id, self.filiere.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"] if "results" in response.data else response.data), 1)

    def test_document_permissions_owner_and_staff(self):
        pdf = SimpleUploadedFile("document.pdf", b"pdf-content", content_type="application/pdf")
        doc = Document.objects.create(
            code_document="DOC005",
            titre="Titre privé",
            resume="Résumé privé",
            fichier=pdf,
            annee_publication=2022,
            statut="Brouillon",
            id_categorie=self.categorie,
            id_filiere=self.filiere,
            id_utilisateur=self.user,
        )

        other_user = User.objects.create_user(
            email="other@example.com",
            password="StrongPass123!",
            first_name="Other",
            last_name="User",
        )

        self.client.force_authenticate(user=other_user)
        response = self.client.patch(f"/api/documents/{doc.id_document}/", {"titre": "Hacked"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.staff)
        staff_response = self.client.patch(f"/api/documents/{doc.id_document}/", {"titre": "By staff"}, format="json")
        self.assertEqual(staff_response.status_code, status.HTTP_200_OK)
