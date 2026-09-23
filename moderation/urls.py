from django.urls import path

from .views import ValidationViewSet

urlpatterns = [
    path("", ValidationViewSet.as_view({"get": "list", "post": "create"})),
    path("<int:pk>/", ValidationViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"})),
    path("<int:pk>/accept/", ValidationViewSet.as_view({"post": "accept_validation"})),
    path("<int:pk>/reject/", ValidationViewSet.as_view({"post": "reject_validation"})),
    path("<int:pk>/archive/", ValidationViewSet.as_view({"post": "archive_validation"})),
    path("document/", ValidationViewSet.as_view({"get": "by_document"})),
]
