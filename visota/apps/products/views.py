from django.shortcuts import render
from rest_framework import viewsets, generics, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q

from .models import *
from .serializers import *

class ProductAPIListPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 50
    
class ProductApi(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.translated().order_by("-id")
    serializer_class = ProductSerializer
    pagination_class = ProductAPIListPagination
    lookup_field = 'translations__slug'

    def get_queryset(self):
        queryset = Product.objects.translated().order_by("translations__priority")

        query_params = self.request.query_params

        pks = query_params.getlist('pk')
        if pks is not None and len(pks) > 0:
            return queryset.filter(pk__in=pks)

        subs = query_params.getlist("sub")
        if subs is not None and len(subs) > 0:
            queryset = queryset.filter(sub_categories__slug__in=subs)

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
    def categories(self, request):
        categories = Category.objects.translated().order_by('priority')
        categoriesSerializer = CategorySerializer(categories, many=True)
        return Response(categoriesSerializer.data)
    
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
