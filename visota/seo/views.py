from django.shortcuts import render, HttpResponse
from rest_framework import viewsets, generics, mixins
from .models import *
from .serializers import SEOStaticPageSerializer, SEOCategoryPageSerializer, SEOProductPageSerializer, SEOPostPageSerializer

# Create your views here.
def robots(req):
  robots = Robots.objects.all()[0]
  return HttpResponse(robots.text, content_type='text/plain')

class MetaStaticApi(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
  queryset = SEOStaticPage.objects.translated()
  serializer_class = SEOStaticPageSerializer
  lookup_field = 'page'


class MetaCategoryApi(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
  queryset = SEOCategoryPage.objects.translated()
  serializer_class = SEOCategoryPageSerializer
  lookup_field = 'category__translations__slug'


class MetaProductApi(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
  queryset = SEOProductPage.objects.translated()
  serializer_class = SEOProductPageSerializer
  lookup_field = 'product__translations__slug'


class MetaPostApi(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
  queryset = SEOPostPage.objects.translated()
  serializer_class = SEOPostPageSerializer
  lookup_field = 'post__translations__slug'