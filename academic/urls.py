from rest_framework.routers import DefaultRouter

from .views import (
    CategorieViewSet,
    FacultéViewSet,
    DépartementViewSet,
    FilièreViewSet,
)


router = DefaultRouter()

router.register(r"facultes", FacultéViewSet, basename="faculte")
router.register(r"departements", DépartementViewSet, basename="departement")
router.register(r"filieres", FilièreViewSet, basename="filiere")
router.register(r"categories", CategorieViewSet, basename="categorie")


urlpatterns = router.urls