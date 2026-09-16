from django.shortcuts import render
from rest_framework import viewsets

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


class DépartementViewSet(viewsets.ModelViewSet):
    queryset = Département.objects.all()
    serializer_class = DépartementSerializer


class FilièreViewSet(viewsets.ModelViewSet):
    queryset = Filière.objects.all()
    serializer_class = FilièreSerializer


class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer