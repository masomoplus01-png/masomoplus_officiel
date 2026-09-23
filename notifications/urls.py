from django.urls import path

from .views import NotificationViewSet

urlpatterns = [
    path("", NotificationViewSet.as_view({"get": "list", "post": "create"})),
    path("<int:pk>/", NotificationViewSet.as_view({"get": "retrieve", "patch": "partial_update"})),
    path("<int:pk>/read/", NotificationViewSet.as_view({"patch": "mark_as_read"})),
]
