import re
from rest_framework import serializers

from .models import *
    

class CommonSerializer(serializers.ModelSerializer):

    def validate_number(self, number):
        result = re.match(r'(^[\+][0-9]{1}[0-9]{3}[0-9]{7}$)', number)
        if result is None:
            raise serializers.ValidationError('Номер телефона должен быть в форме: +79876543210; укажите код города, если необходимо')
        return number
    


class ConsultationRequestSerializer(CommonSerializer):
    class Meta:
        model = ConsultationRequest
        exclude = ('date',)


class PriceRequestSerializer(CommonSerializer):
    class Meta:
        model = PriceRequest
        exclude = ('date',)


class ProductOrderSerializer(serializers.ModelSerializer):
    order_price = serializers.SerializerMethodField('get_current_price')

    class Meta:
        model = ProductOrder
        exclude = ('order', )

    def get_current_price(self, productOrder):
        print(type(productOrder))
        current_price = productOrder.product.current_price
        return current_price


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
            'payment_method',
            'products',
        )

    def create(self, validated_data):
        products = validated_data.pop("products")
        ModelClass = self.Meta.model
        instance = ModelClass.objects.create(**validated_data)
        print(type(products[0]))
        ProductOrder.objects.bulk_create([ProductOrder(**product, order_price=product['product'].current_price, order=instance) for product in products])
        

        return instance


