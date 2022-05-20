from rest_framework.viewsets import ModelViewSet

from API.serializers import UserSerializers, ProductSerializer
from alsodev.models import User, Product


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializers
    queryset = User.objects.all()

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
