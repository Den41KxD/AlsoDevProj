from alsodev.models import User, Product
from rest_framework import serializers
from alsodev.models import Picture


def photo_save(request, product):
    all_images = request.FILES
    for one_image in all_images:
        Picture.objects.create(image=all_images.get(one_image), product_to=product)


class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class PictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Picture
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data.update({'author_id': request.user.id})
        product = Product.objects.create(**validated_data)
        product.author = request.user
        photo_save(request, product)
        return product
