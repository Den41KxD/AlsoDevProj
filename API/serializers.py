from alsodev.models import User, Product
from rest_framework import serializers


class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id','name','price']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data.update({'author_id': request.user.id})
        product = Product.objects.create(**validated_data)
        product.author = request.user
        return product