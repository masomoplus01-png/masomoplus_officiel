from django.urls import path

from .views import AuteurViewSet, DocumentAuteurViewSet

urlpatterns = [
    path("auteurs/", AuteurViewSet.as_view({"get": "list", "post": "create"})),
    path("auteurs/<int:pk>/", AuteurViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"})),
    path("document-auteurs/", DocumentAuteurViewSet.as_view({"get": "list", "post": "add_author_to_document"})),
    path("document-auteurs/<int:pk>/", DocumentAuteurViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"})),
    path("document-auteurs/<int:pk>/update-role/", DocumentAuteurViewSet.as_view({"patch": "update_author_role"})),
    path("document-auteurs/<int:pk>/remove/", DocumentAuteurViewSet.as_view({"delete": "remove_author"})),
]
