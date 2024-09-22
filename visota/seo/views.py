from django.shortcuts import render, HttpResponse
from rest_framework import viewsets, generics, mixins
from .models import *
from .serializers import SEOStaticPageSerializer

# Create your views here.
def robots(req):
  robots = Robots.objects.all()[0]
  return HttpResponse(robots.text, content_type='text/plain')

class MetaStaticApi(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
  queryset = SEOStaticPage.objects.translated()
  serializer_class = SEOStaticPageSerializer
  lookup_field = 'page'