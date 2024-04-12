from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers

from .models import *


class ContentFieldSerializer(serializers.Field):
    def to_representation(self, value):
        domain = 'http://'+str(get_current_site(self.context['request']))
        if self.context['request'].is_secure():
            domain = 'https://'+str(get_current_site(self.context['request']))
        content = value.replace("src=\"/media/", f"src=\"{domain}/media/")
        content = content.replace("&lt;", "<")
        content = content.replace("&gt;", ">")
        content = content.replace("&quot;", "")
        return content


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


class ProductDocsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductDoc
        fields = (
            'id',
            'doc_url',
            'file_name'
        )


class ProductSerializer(serializers.ModelSerializer):
    charachteristics = CharachteristicSerializer(many=True)
    img_urls = ProductImgsSerializer(many=True)
    doc_urls = ProductDocsSerializer(many=True)
    description = ContentFieldSerializer()

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
            'doc_urls',
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