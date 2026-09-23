from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from academic.models import Categorie, Département, Faculté, Filière
from authors.models import Auteur, DocumentAuteur
from documents.models import Document


class AuthorAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="docuser@example.com",
            password="StrongPass123!",
            first_name="Doc",
            last_name="User",
        )
        self.categorie = Categorie.objects.create(code_categorie="CAT2", nom="Article")
        self.faculte = Faculté.objects.create(code_faculte="FAC2", nom="Faculté des Mathématiques")
        self.departement = Département.objects.create(
            code_departement="DEP2",
            nom="Département Mathématiques",
            faculte=self.faculte,
        )
        self.filiere = Filière.objects.create(
            code_filiere="FIL2",
            nom="Mathématiques",
            département=self.departement,
        )
        self.pdf = SimpleUploadedFile("paper.pdf", b"pdf-content", content_type="application/pdf")
        self.document = Document.objects.create(
            code_document="DOC100",
            titre="Thèse de test",
            resume="Résumé test",
            fichier=self.pdf,
            annee_publication=2026,
            statut="Attente",
            id_categorie=self.categorie,
            id_filiere=self.filiere,
            id_utilisateur=self.user,
        )

    def test_create_author(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/authors/auteurs/",
            {
                "code_auteur": "AUT001",
                "nom": "Mbuyi",
                "postnom": "Kashala",
                "prenom": "Jean",
                "email": "jean@example.com",
                "affiliation": "Université de Kinshasa",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Auteur.objects.count(), 1)

    def test_document_author_association(self):
        auteur = Auteur.objects.create(
            code_auteur="AUT002",
            nom="Ngoma",
            prenom="Alice",
            email="alice@example.com",
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/authors/document-auteurs/",
            {
                "id_document": self.document.id_document,
                "id_auteur": auteur.id_auteur,
                "ordre_auteur": 1,
                "role_auteur": "Auteur",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DocumentAuteur.objects.count(), 1)

    def test_multiple_authors_and_role_update(self):
        auteur1 = Auteur.objects.create(code_auteur="AUT003", nom="A", prenom="One")
        auteur2 = Auteur.objects.create(code_auteur="AUT004", nom="B", prenom="Two")
        relation = DocumentAuteur.objects.create(
            id_document=self.document,
            id_auteur=auteur1,
            ordre_auteur=1,
            role_auteur="Auteur",
        )
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            "/api/authors/document-auteurs/",
            {
                "id_document": self.document.id_document,
                "id_auteur": auteur2.id_auteur,
                "ordre_auteur": 2,
                "role_auteur": "Co-auteur",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        update = self.client.patch(
            f"/api/authors/document-auteurs/{relation.id_document_auteur}/update-role/",
            {"role_auteur": "Directeur"},
            format="json",
        )
        self.assertEqual(update.status_code, status.HTTP_200_OK)
        self.assertEqual(update.data["role_auteur"], "Directeur")

    def test_remove_document_author_association(self):
        auteur = Auteur.objects.create(code_auteur="AUT005", nom="C", prenom="Three")
        relation = DocumentAuteur.objects.create(
            id_document=self.document,
            id_auteur=auteur,
            ordre_auteur=1,
            role_auteur="Auteur",
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/authors/document-auteurs/{relation.id_document_auteur}/remove/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DocumentAuteur.objects.filter(pk=relation.pk).exists())
