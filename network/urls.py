from rest_framework.routers import DefaultRouter

from network.views import NetworkNodeViewSet

router = DefaultRouter()
router.register(r"network", NetworkNodeViewSet, basename="network")
urlpatterns = router.urls