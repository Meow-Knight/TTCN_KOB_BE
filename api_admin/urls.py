from django.urls import path
from rest_framework import routers

from api_admin.views import AdminViewSet

app_name = 'api_admin'
router = routers.SimpleRouter(trailing_slash=True)
router.register(r'', AdminViewSet, basename='admin')

urlpatterns = router.urls
