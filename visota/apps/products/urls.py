from django.urls import path, include
from rest_framework import routers


from .views import *

router = routers.SimpleRouter(trailing_slash=True)
router.register('products', ProductApi)
router.register('categories', CategoryApi)
router.register('tags', TagApi)

urlpatterns = [
    path('', include(router.urls)),
    # path('preview/', ProductGroupedByCategoryApi.as_view(), name="products_preview")
]