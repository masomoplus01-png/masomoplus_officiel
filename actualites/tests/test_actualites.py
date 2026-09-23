from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User


PNG_BYTES = BytesIO()
Image.new("RGB", (1, 1), "white").save(PNG_BYTES, format="PNG")
PNG_BYTES = PNG_BYTES.getvalue()


class ActualitesAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="author@example.com",
            password="StrongPass123!",
            first_name="Author",
            last_name="User",
        )
        self.other = User.objects.create_user(
            email="other@example.com",
            password="StrongPass123!",
            first_name="Other",
            last_name="User",
        )

    def test_actualite_create_and_read(self):
        from actualites.models import Actualite

        image = SimpleUploadedFile("cover.png", PNG_BYTES, content_type="image/png")
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/actualites/",
            {"code_actualite": "ACT1", "titre": "Nouvelle actualité", "contenu": "Contenu", "image": image},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Actualite.objects.count(), 1)

        article = Actualite.objects.get(code_actualite="ACT1")
        self.assertEqual(article.id_auteur, self.user)

        detail = self.client.get(f"/api/actualites/{article.id_actualite}/")
        self.assertEqual(detail.status_code, status.HTTP_200_OK)

    def test_actualite_update_delete(self):
        from actualites.models import Actualite

        article = Actualite.objects.create(
            code_actualite="ACT2",
            titre="Ancien titre",
            contenu="Ancien contenu",
            image="https://example.com/image.png",
            id_auteur=self.user,
        )
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(f"/api/actualites/{article.id_actualite}/", {"titre": "Nouveau titre"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["titre"], "Nouveau titre")

        delete_response = self.client.delete(f"/api/actualites/{article.id_actualite}/")
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_actualite_permissions(self):
        from actualites.models import Actualite

        article = Actualite.objects.create(
            code_actualite="ACT3",
            titre="Secret",
            contenu="Contenu",
            image="https://example.com/secret.png",
            id_auteur=self.user,
        )
        self.client.force_authenticate(user=self.other)

        response = self.client.patch(f"/api/actualites/{article.id_actualite}/", {"titre": "Hacked"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
