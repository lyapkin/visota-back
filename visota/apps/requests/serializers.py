import re
from rest_framework import serializers
from .signals import request_save_handlers

from .models import *
    

class CommonSerializer(serializers.ModelSerializer):

    def validate_number(self, number):
        result = re.match(r'^\+?1?\d{9,15}$', number)
        if result is None:
            raise serializers.ValidationError('Номер телефона указан неверно')
        return number
    


class ConsultationRequestSerializer(CommonSerializer):
    class Meta:
        model = ConsultationRequest
        exclude = ('date',)


class OfferRequestSerializer(CommonSerializer):
    class Meta:
        model = OfferRequest
        exclude = ('date',)


class PriceRequestSerializer(CommonSerializer):
    class Meta:
        model = PriceRequest
        exclude = ('date',)


class ProductOrderSerializer(serializers.ModelSerializer):
    # order_price = serializers.SerializerMethodField('get_current_price')

    class Meta:
        model = ProductOrder
        fields = ('product', 'count', 'order_price')

    # def get_current_price(self, productOrder):
    #     print(type(productOrder))
    #     current_price = productOrder.product.current_price
    #     return current_price
    


class OrderSerializer(CommonSerializer):
    products = ProductOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'name',
            'number',
            'email',
            'comment',
            'delivery_address',
            # 'payment_method',
            'products',
        )

    # def validate_payment_method(self, method):
    #     if (method != 'cash') and (method != 'non-cash'):
    #         raise serializers.ValidationError('Выберите способ оплаты')
    #     return method
    
    def validate_products(self, products):
        products_dict = {}
        for p in products:
            products_dict[p['product'].id] = p['order_price']
        queryset = Product.objects.filter(pk__in=map(lambda product: product['product'].id, products))
        for p in queryset.iterator():
            if p.current_price is not products_dict[p.id]:
                raise serializers.ValidationError('Цена на один или несколько продуктов изменилась. Перезагрузите страницу.')
        return products

    def create(self, validated_data):
        products = validated_data.pop("products")
        ModelClass = self.Meta.model
        instance = ModelClass.objects.create(**validated_data)
        ProductOrder.objects.bulk_create([ProductOrder(**product, order=instance) for product in products])
        request_save_handlers.order_ready.send(ModelClass, instance=instance, created=True)

        return instance


class SampleRequestSerializer(CommonSerializer):
    class Meta:
        model = SampleRequest
        exclude = ('date',)