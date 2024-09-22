from django.urls import path, include
from rest_framework import routers


from .views import *

router = routers.SimpleRouter(trailing_slash=True)
router.register('static', MetaStaticApi)

urlpatterns = [
    path('meta/', include(router.urls)),
]