from django.urls import path

from .views import ProjetViewSet

urlpatterns = [
    path("", ProjetViewSet.as_view({"get": "list", "post": "create"})),
    path("<int:pk>/", ProjetViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"})),
]
