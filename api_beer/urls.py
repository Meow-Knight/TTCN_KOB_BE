from rest_framework import routers

from api_beer.views import CreateProducerViewSet, BeerUnitViewSet, NationViewSet, BeerViewSet, BeerShipmentViewSet, \
    BeerPhotoViewSet, CartViewSet

app_name = 'api_beer'
router = routers.SimpleRouter(trailing_slash=True)
router.register(r'producer', CreateProducerViewSet, basename='producer')
router.register(r'unit', BeerUnitViewSet, basename='beer_unit')
router.register(r'nation', NationViewSet, basename='nation')
router.register(r'photo', BeerPhotoViewSet, basename='beer_photo')
router.register(r'shipment', BeerShipmentViewSet, basename='beer_shipment')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'', BeerViewSet, basename='beer')

urlpatterns = router.urls
