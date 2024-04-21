from django.urls import path, include


urlpatterns = [
    path('vacancies/', include('apps.vacancies.urls')),
    path('projects/', include('apps.our_projects.urls')),
    path('promos/', include('apps.promos.urls')),
    path('request/', include('apps.requests.urls')),
]

urlpatterns += i18n_patterns(
    path('products/', include('apps.products.urls')),
    path('articles/', include('apps.blog.urls')),
    path('faq/', include('apps.faq.urls')),
) 