import math
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from rest_framework import viewsets, generics, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q

from .models import *
from .serializers import *

class ProductAPIListPagination(PageNumberPagination):
    page_size = 12

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['page_count'] = math.ceil(response.data['count'] / self.get_page_size(self.request))
        return response
    
class ProductApi(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.translated().order_by("-id")
    serializer_class = ProductSerializer
    pagination_class = ProductAPIListPagination
    lookup_field = 'translations__slug'

    def get_queryset(self):
        queryset = Product.objects.translated().order_by("translations__priority", 'id')

        query_params = self.request.query_params

        pks = query_params.getlist('pk')
        if pks is not None and len(pks) > 0:
            return queryset.filter(pk__in=pks)

        # sub = query_params.get("sub")
        # if sub is not None:
        #     queryset = queryset.filter(sub_categories__slug=sub)

        price_min = query_params.get('price_min')
        price_max = query_params.get('price_max')
        price_min_valid = True
        price_max_valid = True

        try:
            price_min = int(price_min)
        except:
            price_min_valid = False

        try:
            price_max = int(price_max)
        except:
            price_max_valid = False


        if price_max_valid and price_min_valid:
            queryset = queryset.filter(current_price__range=[price_min, price_max])
        elif price_max_valid:
            queryset = queryset.filter(current_price__lte=price_max)
        elif price_min_valid:
            queryset = queryset.filter(current_price__gte=price_min)

        searchline = query_params.get('search')
        searchline = searchline.strip() if isinstance(searchline, str) else None
        if searchline is not None:
            searchline = searchline.split()
            queryset = queryset.filter(*[Q(translations__name__icontains=q) for q in searchline])

        return queryset

    
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


class CategoryApi(viewsets.ReadOnlyModelViewSet):
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

    @action(detail=True)
    def exists(self, request, slug=None):
        # get_object_or_404(SubCategory, translations__slug=slug)
        try:
          SubCategory.objects.get(translations__slug=slug)
          return Response()
        except SubCategory.DoesNotExist:
          # return redirect('http://localhost:3000/', permanent=True)
          response = HttpResponse(status=301)
          response['Location'] = 'http://loclahost:8000/ru/api'
          return response

    @action(detail=True, serializer_class=ProductSerializer, pagination_class = ProductAPIListPagination)
    def products(self, request, slug=None):
        # category = get_object_or_404(SubCategory, translations__slug=slug)
        try:
          category = SubCategory.objects.get(translations__slug=slug)
        except SubCategory.DoesNotExist:
          return redirect('https://visota13.ru/', permanent=True)
          # response = HttpResponse(status=301)
          # response['Location'] = 'https://visota13.ru/'
          # return response
        
        products = category.products.translated().all()

        products = self.filter(products)

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(products, many=True)
        
        return Response(serializer.data)
    

    def filter(self, queryset):

        query_params = self.request.query_params

        pks = query_params.getlist('pk')
        if pks is not None and len(pks) > 0:
            return queryset.filter(pk__in=pks)

        price_min = query_params.get('price_min')
        price_max = query_params.get('price_max')
        price_min_valid = True
        price_max_valid = True

        try:
            price_min = int(price_min)
        except:
            price_min_valid = False

        try:
            price_max = int(price_max)
        except:
            price_max_valid = False


        if price_max_valid and price_min_valid:
            queryset = queryset.filter(current_price__range=[price_min, price_max])
        elif price_max_valid:
            queryset = queryset.filter(current_price__lte=price_max)
        elif price_min_valid:
            queryset = queryset.filter(current_price__gte=price_min)

        searchline = query_params.get('search')
        searchline = searchline.strip() if isinstance(searchline, str) else None
        if searchline is not None:
            searchline = searchline.split()
            queryset = queryset.filter(*[Q(translations__name__icontains=q) for q in searchline])

        return queryset
    