from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

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


class CharachteristicSerializer(TranslatableModelSerializer):
    # char = serializers.StringRelatedField()
    translations = TranslatedFieldsField(shared_model=CharValue)

    class Meta:
        model = CharValue
        fields = (
            'id',
            # 'key',
            # 'value',
            'translations',
        )


class ProductImgsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImg
        fields = (
            'id',
            'img_url'
        )


# class ProductDocsSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = ProductDoc
#         fields = (
#             'id',
#             'doc_url',
#             'file_name'
#         )


class ProductSerializer(serializers.ModelSerializer):
    charachteristics = CharachteristicSerializer(many=True)
    img_urls = ProductImgsSerializer(many=True)
    # doc_urls = ProductDocsSerializer(many=True)
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
            # 'doc_urls',
            'is_present'
        )
        lookup_field = 'slug'


class SubcategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=SubCategory)

    class Meta:
        model = SubCategory
        fields = ('id', 'slug', 'translations')


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('name', 'id', 'slug', 'subcategories')