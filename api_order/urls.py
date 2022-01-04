from rest_framework import routers

from api_order.views.Order import OrderViewSet

app_name = 'api_admin'
router = routers.SimpleRouter(trailing_slash=True)
router.register(r'', OrderViewSet, basename='order')

urlpatterns = router.urls
