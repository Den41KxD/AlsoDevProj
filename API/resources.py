import os
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from API.serializers import UserSerializers, ProductSerializer, PictureSerializer, photo_save
from alsodev.models import User, Product, Picture


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializers
    queryset = User.objects.all()


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        for product_item in serializer.data:
            product_item.update({'photo': self.get_image(product_item.get('id'))})

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        photo = self.get_image(serializer.data.get('id'))
        return Response((serializer.data, photo))

    def get_image(self, product_id):
        save_serialiser = self.get_serializer()
        self.serializer_class = PictureSerializer
        all_photo = Picture.objects.filter(product_to_id=product_id)
        serializer = self.get_serializer(all_photo, many=True)
        self.serializer_class = save_serialiser
        return serializer.data

    def destroy(self, request, *args, **kwargs):
        product_name = Product.objects.get(id=kwargs['pk'])
        if product_name.author == request.user or request.user.is_superuser:

            image_to_delete = Picture.objects.filter(product_to_id=kwargs['pk'])
            for image in image_to_delete:
                os.remove(f"media/{image.image}")
            path_to_media = f"media/{str(product_name.id)}/"
            if os.access(path_to_media, os.R_OK and os.X_OK):
                os.removedirs(path_to_media)

            return super(ProductViewSet, self).destroy(request)
        else:
            return Response('You can\'t delete this product')

    def partial_update(self, request, *args, **kwargs):
        product_name = Product.objects.get(id=kwargs['pk'])
        if product_name.author == request.user or request.user.is_superuser:
            my_response=super(ProductViewSet, self).partial_update(request)

            if my_response.status_code == 200:
                photo_save(request, product_name)
            return my_response
        else:
            return Response('You can\'t update this product')

    def update(self, request, *args, **kwargs):
        if request.stream.method == 'PATCH':
            return super(ProductViewSet, self).update(request)
        else:
            product_name = Product.objects.get(id=kwargs['pk'])
            if product_name.author == request.user or request.user.is_superuser:
                response = super(ProductViewSet, self).update(request)

                if response.status_code == 200:
                    image_to_delete = Picture.objects.filter(product_to_id=kwargs['pk'])
                    for image in image_to_delete:
                        os.remove(f"media/{image.image}")
                        image.delete()
                    photo_save(request, product_name)

                return response
            else:
                return Response('You can\'t update this product')
