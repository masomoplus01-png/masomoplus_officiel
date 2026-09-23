from django.test import TestCase
from rest_framework.test import APIClient


class TestModeSecurityAccess(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthenticated_get_endpoints_are_open(self):
        for url in [
            "/api/academic/facultes/",
            "/api/documents/",
            "/api/analytics/",
            "/api/moderation/",
            "/api/interactions/telechargements/",
            "/api/interactions/commentaires/",
            "/api/projets/",
            "/api/notifications/",
            "/api/support/",
            "/api/actualites/",
        ]:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 500, msg=f"{url} should not crash in test mode")
            self.assertNotEqual(response.status_code, 401, msg=f"{url} should not require auth in test mode")

    def test_unauthenticated_post_endpoints_are_not_forbidden(self):
        response = self.client.post("/api/notifications/", data={}, format="json")
        self.assertNotEqual(response.status_code, 401, msg="POST endpoint should not require auth in test mode")
