from rest_framework import routers

app_name = 'api_account'
router = routers.SimpleRouter(trailing_slash=True)
# router.register(r'favourite_plant', FavouritePlantViewSet, basename='favourite_plants')

urlpatterns = router.urls
