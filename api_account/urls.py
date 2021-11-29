from rest_framework import routers

from api_account.views import RoleViewSet

app_name = 'api_account'
router = routers.SimpleRouter(trailing_slash=True)
router.register(r'role1', RoleViewSet, basename='role')

urlpatterns = router.urls
