from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Categorie, Faculté, Département, Filière
from .serializers import (
    CategorieSerializer,
    FacultéSerializer,
    DépartementSerializer,
    FilièreSerializer,
)


class FacultéViewSet(viewsets.ModelViewSet):
    queryset = Faculté.objects.all()
    serializer_class = FacultéSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class DépartementViewSet(viewsets.ModelViewSet):
    queryset = Département.objects.all()
    serializer_class = DépartementSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class FilièreViewSet(viewsets.ModelViewSet):
    queryset = Filière.objects.all()
    serializer_class = FilièreSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [AllowAny]
    pagination_class = None