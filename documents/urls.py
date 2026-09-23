from django.urls import path

from .views import DocumentViewSet

urlpatterns = [
    path("", DocumentViewSet.as_view({"get": "list", "post": "create"})),
    path("<int:pk>/", DocumentViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"})),
    path("<int:pk>/status/", DocumentViewSet.as_view({"patch": "update_status"})),
]
