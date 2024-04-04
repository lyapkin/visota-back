from rest_framework import serializers

from .models import *


class CharachteristicSerializer(serializers.ModelSerializer):
    char = serializers.StringRelatedField()

    class Meta:
        model = CharValue
        fields = (
            'id',
            'char',
            'value'
        )


class ProductImgsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImg
        fields = (
            'id',
            'img_url'
        )


class ProductSerializer(serializers.ModelSerializer):
    charachteristics = CharachteristicSerializer(many=True)
    img_urls = ProductImgsSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "code",
            "slug",
            "actual_price",
            "current_price",
            "charachteristics",
            "description",
            "img_urls",
            'is_present'
        )
        lookup_field = 'slug'


class SubcategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        exclude = ('category',)


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'