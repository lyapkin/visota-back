from rest_framework import viewsets, mixins

from .models import *
from .serializers import *
        

class ConsultationRequestApi(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = ConsultationRequest.objects.all()
    serializer_class = ConsultationRequestSerializer


class PriceRequestApi(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = PriceRequest.objects.all()
    serializer_class = PriceRequestSerializer


class OrderApi(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer