from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import Http404
from django.utils.translation import get_language
from rest_framework import viewsets, generics, mixins
from .models import *
from .serializers import (
    SEOStaticPageSerializer,
    SEOCategoryPageSerializer,
    SEOTagPageSerializer,
    SEOProductPageSerializer,
    SEOPostPageSerializer,
    SitemapSerializer,
)
from apps.products.models import ProductRedirectFrom, CategoryRedirectFrom, TagRedirectFrom
from apps.blog.models import PostRedirectFrom


# Create your views here.
def robots(req):
    robots = Robots.objects.all()[0]
    return HttpResponse(robots.text, content_type="text/plain")


class MetaStaticApi(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = SEOStaticPage.objects.translated()
    serializer_class = SEOStaticPageSerializer
    lookup_field = "page"


class MetaCategoryApi(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = SEOCategoryPage.objects.all()
    serializer_class = SEOCategoryPageSerializer
    lookup_field = "category__translations__slug"

    def get_object(self):
        try:
            obj = super().get_object()
        except Http404:
            slug = self.kwargs[self.lookup_url_kwarg]
            redirect = get_object_or_404(CategoryRedirectFrom, lang=get_language(), old_slug=slug)
            obj = redirect.to.seo
        return obj


class MetaTagApi(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = SEOTagPage.objects.all()
    serializer_class = SEOTagPageSerializer
    lookup_field = "tag__translations__slug"

    def get_object(self):
        try:
            obj = super().get_object()
        except Http404:
            slug = self.kwargs[self.lookup_url_kwarg]
            redirect = get_object_or_404(TagRedirectFrom, lang=get_language(), old_slug=slug)
            obj = redirect.to.seo
        return obj


class MetaProductApi(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = SEOProductPage.objects.all()
    serializer_class = SEOProductPageSerializer
    lookup_field = "product__translations__slug"
    lookup_url_kwarg = "slug"

    def get_object(self):
        try:
            obj = super().get_object()
        except Http404:
            slug = self.kwargs[self.lookup_url_kwarg]
            redirect = get_object_or_404(ProductRedirectFrom, lang=get_language(), old_slug=slug)
            obj = redirect.to.seo
        return obj


class MetaPostApi(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = SEOPostPage.objects.all()
    serializer_class = SEOPostPageSerializer
    lookup_field = "post__translations__slug"

    def get_object(self):
        try:
            obj = super().get_object()
        except Http404:
            slug = self.kwargs[self.lookup_url_kwarg]
            redirect = get_object_or_404(PostRedirectFrom, lang=get_language(), old_slug=slug)
            obj = redirect.to.seo
        return obj


class SitemapApi(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Sitemap.objects.all()
    serializer_class = SitemapSerializer

    def get_object(self):
        return self.get_queryset().first()
