from django.urls import path, include


urlpatterns = [
    path('products/', include('apps.products.urls')),
    path('articles/', include('apps.blog.urls')),
]