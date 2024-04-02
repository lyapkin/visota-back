from django.urls import path, include
from rest_framework import routers


from .views import *

router = routers.SimpleRouter(trailing_slash=False)
router.register('', ProductApi)

urlpatterns = [
    path('', include(router.urls)),
    # path('preview/', ProductGroupedByCategoryApi.as_view(), name="products_preview")
]