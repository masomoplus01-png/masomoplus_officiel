from django.urls import path

from .views import ActualiteViewSet

urlpatterns = [
    path("", ActualiteViewSet.as_view({"get": "list", "post": "create"})),
    path("<int:pk>/", ActualiteViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"})),
]
