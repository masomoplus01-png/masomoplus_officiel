from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Faculté, Département, Filière, Categorie


class AcademicAPITests(APITestCase):

    def test_create_faculte(self):
        data = {
            "code_faculte": "TEST",
            "nom": "Faculté de Test",
            "déscription": "Faculté créée pour tester l'API.",
        }

        response = self.client.post(
            "/api/academic/facultes/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["code_faculte"], "TEST")

    def test_create_departement_lie_a_faculte(self):
        faculte = Faculté.objects.create(
            code_faculte="FASI",
            nom="Faculté des Sciences Informatiques"
        )

        data = {
            "code_departement": "INFO",
            "nom": "Département d'Informatique",
            "déscription": "Département chargé de la formation en informatique",
            "faculte": faculte.id,
        }

        response = self.client.post(
            "/api/academic/departements/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["faculte"], faculte.id)

    def test_create_filiere_liee_a_departement(self):
        faculte = Faculté.objects.create(
            code_faculte="FASI",
            nom="Faculté des Sciences Informatiques"
        )

        departement = Département.objects.create(
            code_departement="INFO",
            nom="Département d'Informatique",
            faculte=faculte
        )

        data = {
            "code_filiere": "DEV",
            "nom": "Génie logiciel et développement",
            "déscription": "Filière consacrée au développement logiciel",
            "département": departement.id,
        }

        response = self.client.post(
            "/api/academic/filieres/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["département"],
            departement.id
        )

    def test_create_categorie(self):
        data = {
            "code_categorie": "MEM",
            "nom": "Mémoire",
            "déscription": "Travail scientifique réalisé dans le cadre de la fin des études",
        }

        response = self.client.post(
            "/api/academic/categories/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["code_categorie"], "MEM")

    def test_get_facultes(self):
        Faculté.objects.create(
            code_faculte="FASI",
            nom="Faculté des Sciences Informatiques"
        )

        response = self.client.get(
            "/api/academic/facultes/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_faculte_put(self):
        faculte = Faculté.objects.create(
            code_faculte="FASI",
            nom="Ancien nom"
        )

        data = {
            "code_faculte": "FASI",
            "nom": "Faculté des Sciences Informatiques",
            "déscription": "Nouvelle description",
        }

        response = self.client.put(
            f"/api/academic/facultes/{faculte.id}/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["nom"],
            "Faculté des Sciences Informatiques"
        )

    def test_update_faculte_patch(self):
        faculte = Faculté.objects.create(
            code_faculte="FASI",
            nom="Ancien nom"
        )

        data = {
            "nom": "Nouveau nom"
        }

        response = self.client.patch(
            f"/api/academic/facultes/{faculte.id}/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["nom"],
            "Nouveau nom"
        )

    def test_delete_faculte(self):
        faculte = Faculté.objects.create(
            code_faculte="TEST",
            nom="Faculté temporaire"
        )

        response = self.client.delete(
            f"/api/academic/facultes/{faculte.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Faculté.objects.filter(id=faculte.id).exists()
        )