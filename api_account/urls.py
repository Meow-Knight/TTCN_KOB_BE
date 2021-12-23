from rest_framework import routers

from api_account.views import RoleViewSet, AccountViewSet

app_name = 'api_account'
router = routers.SimpleRouter(trailing_slash=True)
router.register(r'', AccountViewSet, basename='account')
router.register(r'role', RoleViewSet, basename='role')

urlpatterns = router.urls
