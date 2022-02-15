from django.urls import path, include
from .views import OfferListView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('offers', OfferListView, basename="offers")

urlpatterns = router.urls