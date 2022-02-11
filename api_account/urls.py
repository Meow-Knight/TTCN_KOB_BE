from rest_framework import routers

from api_account.views import RoleViewSet, AccountViewSet, ReviewViewSet

app_name = 'api_account'
router = routers.SimpleRouter(trailing_slash=True)
router.register(r'review', ReviewViewSet, basename='review')
router.register(r'role', RoleViewSet, basename='role')
router.register(r'', AccountViewSet, basename='account')

urlpatterns = router.urls
