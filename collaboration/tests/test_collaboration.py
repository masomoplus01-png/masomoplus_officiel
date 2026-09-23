from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User


class CollaborationAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="StrongPass123!",
            first_name="Owner",
            last_name="User",
        )
        self.other = User.objects.create_user(
            email="member@example.com",
            password="StrongPass123!",
            first_name="Other",
            last_name="User",
        )

    def test_project_create_and_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/projets/",
            {"code_projet": "PRJ1", "titre": "Projet test", "description": "Description", "domaine": "AI", "statut": "Ouvert"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["code_projet"], "PRJ1")

        list_response = self.client.get("/api/projets/")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(list_response.data["count"], 1)

    def test_project_update_and_delete(self):
        from collaboration.models import Projet

        project = Projet.objects.create(
            code_projet="PRJ2",
            titre="Projet initial",
            description="Desc",
            domaine="Data",
            statut="Ouvert",
            id_createur=self.user,
        )
        self.client.force_authenticate(user=self.user)

        patch_response = self.client.patch(f"/api/projets/{project.id_projet}/", {"titre": "Projet modifié"}, format="json")
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.data["titre"], "Projet modifié")

        delete_response = self.client.delete(f"/api/projets/{project.id_projet}/")
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_project_permissions(self):
        from collaboration.models import Projet

        project = Projet.objects.create(
            code_projet="PRJ3",
            titre="Projet secret",
            description="Desc",
            domaine="Data",
            statut="Ouvert",
            id_createur=self.user,
        )
        self.client.force_authenticate(user=self.other)

        response = self.client.patch(f"/api/projets/{project.id_projet}/", {"titre": "Hacked"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_project_creator_and_status(self):
        from collaboration.models import Projet

        project = Projet.objects.create(
            code_projet="PRJ4",
            titre="Projet status",
            description="Desc",
            domaine="IA",
            statut="En cours",
            id_createur=self.user,
        )
        self.assertEqual(project.id_createur, self.user)
        self.assertEqual(project.statut, "En cours")
