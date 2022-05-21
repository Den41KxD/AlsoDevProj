from django.urls import path, include
from rest_framework.routers import SimpleRouter

from API.resources import UserViewSet, ProductViewSet
from alsodev.views import CustomAuthToken

router = SimpleRouter()
router.register('user', UserViewSet)
router.register('product', ProductViewSet)


urlpatterns = [

    path('api/', include(router.urls)),
    path('api-auth/', CustomAuthToken.as_view())
]
