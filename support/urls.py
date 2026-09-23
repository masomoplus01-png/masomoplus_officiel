from django.urls import path

from .views import SupportViewSet

urlpatterns = [
    path("", SupportViewSet.as_view({"get": "list", "post": "create"})),
    path("<int:pk>/", SupportViewSet.as_view({"get": "retrieve", "patch": "partial_update"})),
]
