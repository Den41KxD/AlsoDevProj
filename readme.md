Created a CRUD (create/read/update/delete) application based on the Django Rest Framework, where the "Product" entity management is implemented.
"Product" has the following data:
1. Title
2. Price
3. Image (one or more)
4. Author (who created the product)
5. Creation date

Application used Postgresql database

Postman commands:

[POST]
http://127.0.0.1:8000/api/user/ create  new user
{
    "username": "username",
    "password": "password"
}

[POST]
http://127.0.0.1:8000/api-auth/ create and get TOKEN

in the future, be sure to add this token to the headers
this token is temporary, if not used it will be deleted after 24 hours

[POST]
http://127.0.0.1:8000/api/product/ create new product 
Fields must be added to the body:
    'name'
    'price'
optionally add fields:
    'image'

[GET]
http://127.0.0.1:8000/api/product/ get all products

[GET]
http://127.0.0.1:8000/api/product/{id} get one product by id

[DELETE]
http://127.0.0.1:8000/api/product/{id} delete one product by id

[PATCH]
http://127.0.0.1:8000/api/product/{id} partial change one product by id

optionally add fields:
    'name'
    'price'
    'image' - new images to add to the current product
    'photo_id_to_delete' - single value or list of images to remove

[PUT]
http://127.0.0.1:8000/api/product/{id} 
Complete change of one product by id, all photos will be deleted.
If you send new photos, they will be added instead of deleted ones

Fields must be added to the body:
    'name'
    'price'
optionally add fields:
    'image'