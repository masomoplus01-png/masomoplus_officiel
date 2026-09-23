from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User


class NotificationsAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            password="StrongPass123!",
            first_name="User",
            last_name="Test",
        )
        self.other = User.objects.create_user(
            email="other@example.com",
            password="StrongPass123!",
            first_name="Other",
            last_name="Test",
        )

    def test_notification_create_and_read(self):
        from notifications.models import Notification

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/notifications/",
            {"code_notification": "NT1", "titre": "Test notif", "contenu": "Bonjour", "type": "Système", "lu": False},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        notification = Notification.objects.get(code_notification="NT1")
        self.assertEqual(notification.id_utilisateur, self.user)

        read_response = self.client.patch(f"/api/notifications/{notification.id_notification}/read/", {}, format="json")
        self.assertEqual(read_response.status_code, status.HTTP_200_OK)
        notification.refresh_from_db()
        self.assertTrue(notification.lu)

    def test_notification_isolation(self):
        from notifications.models import Notification

        self.client.force_authenticate(user=self.user)
        Notification.objects.create(
            code_notification="NT2",
            titre="Notif user",
            contenu="Hello",
            type="Commentaire",
            lu=False,
            id_utilisateur=self.user,
        )
        Notification.objects.create(
            code_notification="NT3",
            titre="Notif other",
            contenu="Hello other",
            type="Système",
            lu=False,
            id_utilisateur=self.other,
        )

        list_response = self.client.get("/api/notifications/")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(list_response.data["count"], 1)

    def test_notification_type_and_lu(self):
        from notifications.models import Notification

        notification = Notification.objects.create(
            code_notification="NT4",
            titre="Type test",
            contenu="Message",
            type="Nouveau document",
            lu=False,
            id_utilisateur=self.user,
        )
        self.assertEqual(notification.type, "Nouveau document")
        self.assertFalse(notification.lu)
        self.assertEqual(notification.id_utilisateur, self.user)
