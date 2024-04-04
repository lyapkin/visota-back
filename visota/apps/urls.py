from django.urls import path, include


urlpatterns = [
    path('products/', include('apps.products.urls')),
    path('articles/', include('apps.blog.urls')),
    path('faq/', include('apps.faq.urls')),
    path('vacancies/', include('apps.vacancies.urls')),
    path('projects/', include('apps.our_projects.urls')),
]