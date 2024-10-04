from django.urls import path, include
from rest_framework import routers


from .views import *

router = routers.SimpleRouter(trailing_slash=True)
router.register('static', MetaStaticApi)
router.register('category', MetaCategoryApi)
router.register('tag', MetaTagApi)
router.register('product', MetaProductApi)
router.register('blog', MetaPostApi)
router.register('sitemap', SitemapApi)

urlpatterns = [
    path('meta/', include(router.urls)),
]