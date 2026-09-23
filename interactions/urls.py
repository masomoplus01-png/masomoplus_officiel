from django.urls import path

from .views import CommentaireViewSet, ConsultationViewSet, FavoriViewSet, TelechargementViewSet

urlpatterns = [
    path("telechargements/", TelechargementViewSet.as_view({"get": "list", "post": "create"})),
    path("telechargements/<int:pk>/", TelechargementViewSet.as_view({"get": "retrieve", "delete": "destroy"})),
    path("consultations/", ConsultationViewSet.as_view({"get": "list", "post": "create"})),
    path("consultations/<int:pk>/", ConsultationViewSet.as_view({"get": "retrieve", "delete": "destroy"})),
    path("favoris/", FavoriViewSet.as_view({"get": "list", "post": "create"})),
    path("favoris/<int:pk>/", FavoriViewSet.as_view({"get": "retrieve", "delete": "destroy"})),
    path("commentaires/", CommentaireViewSet.as_view({"get": "list", "post": "create"})),
    path("commentaires/<int:pk>/", CommentaireViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"})),
]
