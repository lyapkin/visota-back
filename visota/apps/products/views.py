import math
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from rest_framework import viewsets, generics, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q, F
from django.utils.translation import get_language

from .models import *
from .serializers import *
from .mixins import FilterMixin

class ProductAPIListPagination(PageNumberPagination):
    page_size = 12

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['page_count'] = math.ceil(response.data['count'] / self.get_page_size(self.request))
        return response
    
class ProductApi(viewsets.ReadOnlyModelViewSet, FilterMixin):
    queryset = Product.objects.translated().order_by("-id")
    serializer_class = ProductSerializer
    pagination_class = ProductAPIListPagination
    lookup_field = 'translations__slug'
    lookup_url_kwarg = 'slug'

    def retrieve(self, request, slug=None, *args, **kwargs):
        # return super().retrieve(request, *args, **kwargs)
        try:
          instance = self.get_object()
        except Http404:
          active_slug = get_object_or_404(ProductRedirectFrom, lang=get_language(), old_slug=slug)
          return redirect(f'/{active_slug.to.slug}/', permanent=True)
        instance.views = F('views') + 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Product.objects.translated().order_by("translations__priority", 'id')

        return self.filter(queryset=queryset)

    
    @action(detail=False)
    def cart(self, request):
        query_params = request.query_params

        pks = query_params.getlist('pk')
        if pks is not None and len(pks) > 0:
            pks = map(lambda item: int(item), pks)
            queryset = Product.objects.filter(id__in=pks)
            cartSerializer = ProductSerializer(queryset.order_by(*pks), many=True, context={'request': request})
        
            return Response(cartSerializer.data)
        
        return Response(status=404)


class CategoryApi(viewsets.ReadOnlyModelViewSet, FilterMixin):
    queryset = Category.objects.translated().order_by('priority')
    serializer_class = CategorySerializer
    # pagination_class = ProductAPIListPagination
    lookup_field = 'translations__slug'
    lookup_url_kwarg = 'slug'

    # def retrieve(self, request, slug=None, *args, **kwargs):
    #     category = get_object_or_404(SubCategory, translations__slug=slug)
    #     products = category.products.translated().all()

    #     products = self.filter(products)

    #     page = self.paginate_queryset(products)
    #     if page is not None:
    #         serializer = ProductSerializer(page, many=True, context={'request': request})
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(products, many=True, context={'request': request})
        
    #     return Response(serializer.data)

    def retrieve(self, request, slug=None, *args, **kwargs):
        try:
          cat = SubCategory.objects.get(translations__slug=slug)
          return JsonResponse({"name": cat.name, "description": cat.description})
        except SubCategory.DoesNotExist:
          active_slug = get_object_or_404(CategoryRedirectFrom, lang=get_language(), old_slug=slug)
          return redirect(f'/{active_slug.to.slug}/', permanent=True)

    @action(detail=True)
    def exists(self, request, slug=None):
        try:
          cat = SubCategory.objects.get(translations__slug=slug)
          return JsonResponse({"name": cat.name, "description": cat.description})
        except SubCategory.DoesNotExist:
          active_slug = get_object_or_404(CategoryRedirectFrom, lang=get_language(), old_slug=slug)
          return redirect(f'/{active_slug.to.slug}/', permanent=True)

    @action(detail=True, serializer_class=ProductSerializer, pagination_class = ProductAPIListPagination)
    def products(self, request, slug=None):
        category = get_object_or_404(SubCategory, translations__slug=slug)

        products = category.products.filter(translations__language_code=get_language())

        filters = self.request.query_params.getlist('filters')
        if filters is not None and len(filters) > 0:
          products = products.filter(filters__translations__slug__in=filters)

        products = self.filter(products)

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(products, many=True)
        
        return Response(serializer.data)
    

class TagApi(viewsets.ReadOnlyModelViewSet, FilterMixin):
  queryset = Tag.objects.all()
  serializer_class = TagSerializer
  lookup_field = 'translations__slug'
  lookup_url_kwarg = 'slug'

  def get_queryset(self):
    return super().get_queryset().filter(translations__language_code=get_language())

  def retrieve(self, request, slug=None, *args, **kwargs):
    try:
      tag = Tag.objects.get(translations__slug=slug)
      return JsonResponse({"name": tag.name})
    except Tag.DoesNotExist:
      active_slug = get_object_or_404(TagRedirectFrom, lang=get_language(), old_slug=slug)
      return redirect(f'/{active_slug.to.slug}/', permanent=True)

  @action(detail=True, serializer_class=ProductSerializer, pagination_class = ProductAPIListPagination)
  def products(self, request, slug=None):
    tag = get_object_or_404(Tag, translations__slug=slug)
    
    products = tag.products.translated().all()

    products = self.filter(products)

    page = self.paginate_queryset(products)
    if page is not None:
      serializer = self.get_serializer(page, many=True)
      return self.get_paginated_response(serializer.data)

    serializer = self.get_serializer(products, many=True)
    
    return Response(serializer.data)