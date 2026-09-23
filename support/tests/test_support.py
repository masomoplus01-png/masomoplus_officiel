from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User


class SupportAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            password="StrongPass123!",
            first_name="User",
            last_name="Test",
        )
        self.staff = User.objects.create_user(
            email="staff@example.com",
            password="StrongPass123!",
            first_name="Staff",
            last_name="User",
            is_staff=True,
        )

    def test_support_create_and_list(self):
        from support.models import Support

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/support/",
            {"code_support": "SUP1", "sujet": "Bug login", "message": "Je n'arrive pas à me connecter.", "statut": "Ouvert"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Support.objects.count(), 1)

        list_response = self.client.get("/api/support/")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(list_response.data["count"], 1)

    def test_support_resolution_and_update(self):
        from support.models import Support

        ticket = Support.objects.create(
            code_support="SUP2",
            sujet="Problème upload",
            message="L'image ne charge pas.",
            statut="Ouvert",
            id_utilisateur=self.user,
        )
        self.client.force_authenticate(user=self.staff)

        response = self.client.patch(
            f"/api/support/{ticket.id_support}/",
            {"statut": "Résolu", "date_resolution": timezone.now().isoformat()},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["statut"], "Résolu")
        self.assertIsNotNone(response.data["date_resolution"])

    def test_support_user_isolation(self):
        from support.models import Support

        ticket = Support.objects.create(
            code_support="SUP3",
            sujet="Ticket autre",
            message="Différent",
            statut="Ouvert",
            id_utilisateur=self.user,
        )
        self.client.force_authenticate(user=self.staff)
        list_response = self.client.get("/api/support/")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(list_response.data["count"], 1)

    def test_support_permissions(self):
        from support.models import Support

        ticket = Support.objects.create(
            code_support="SUP4",
            sujet="Ticket secret",
            message="secret",
            statut="Ouvert",
            id_utilisateur=self.user,
        )
        self.client.force_authenticate(user=self.staff)
        response = self.client.patch(f"/api/support/{ticket.id_support}/", {"statut": "Résolu"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
