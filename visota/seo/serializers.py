from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

from .models import *


class SEOPageSerializer(TranslatableModelSerializer):
  def to_representation(self, instance):
    translated = instance.has_translation(instance.get_current_language())

    if translated:
      representation = super().to_representation(instance)
      header = representation.get('header', None)
      robots = {
        'index': False,
        'follow': True,
      } if representation['noindex_follow'] else {}
      meta = {
        'title': representation['title'],
        'description': representation['description'],
        'robots': robots
      }
      result = {
        'translated': translated,
        'header': header,
        'meta': meta
      }
      
    else:
      result = {'translated': False}
    
    return result
  

class SEOStaticPageSerializer(SEOPageSerializer):

  class Meta:
    model = SEOStaticPage
    fields = (
      'header',
      'title',
      'description',
      'noindex_follow',
    )


class SEOCategoryPageSerializer(SEOPageSerializer):

  class Meta:
    model = SEOCategoryPage
    fields = (
      'title',
      'description',
      'noindex_follow',
    )


class SEOProductPageSerializer(SEOPageSerializer):

  class Meta:
    model = SEOProductPage
    fields = (
      'title',
      'description',
      'noindex_follow',
    )


class SEOPostPageSerializer(SEOPageSerializer):

  class Meta:
    model = SEOProductPage
    fields = (
      'title',
      'description',
      'noindex_follow',
    )


class SitemapStaticsSerializer(TranslatableModelSerializer):
  
  class Meta:
    model = SEOStaticPage
    fields = (
      'page',
    )


class CategorySlugSerializer(TranslatableModelSerializer):
  translations = TranslatedFieldsField(shared_model=SubCategory)

  class Meta:
    model = SubCategory
    fields = (
      'translations',
    )


class SitemapCategoriesSerializer(TranslatableModelSerializer):
  category = CategorySlugSerializer()

  class Meta:
    model = SEOCategoryPage
    fields = (
      'category',
    )

  def to_representation(self, instance):
    represention = super().to_representation(instance)
    translations = represention['category']['translations']
    result = {}
    for key in translations:
      result[key] = translations[key]['slug']
    return result


class ProductSlugSerializer(TranslatableModelSerializer):
  translations = TranslatedFieldsField(shared_model=Product)

  class Meta:
    model = Product
    fields = (
      'translations',
    )


class SitemapProductsSerializer(TranslatableModelSerializer):
  product = ProductSlugSerializer()

  class Meta:
    model = SEOProductPage
    fields = (
      'product',
    )

  def to_representation(self, instance):
    represention = super().to_representation(instance)
    translations = represention['product']['translations']
    result = {}
    for key in translations:
      result[key] = translations[key]['slug']
    return result


class PostSlugSerializer(TranslatableModelSerializer):
  translations = TranslatedFieldsField(shared_model=Post)

  class Meta:
    model = Post
    fields = (
      'translations',
    )


class SitemapPostsSerializer(TranslatableModelSerializer):
  post = PostSlugSerializer()

  class Meta:
    model = SEOPostPage
    fields = (
      'post',
    )

  def to_representation(self, instance):
    represention = super().to_representation(instance)
    translations = represention['post']['translations']
    result = {}
    for key in translations:
      result[key] = translations[key]['slug']
    return result


class SitemapSerializer(serializers.ModelSerializer):
  # statics = SitemapStaticsSerializer(many=True)
  categories = SitemapCategoriesSerializer(many=True)
  products = SitemapProductsSerializer(many=True)
  posts = SitemapPostsSerializer(many=True)


  class Meta:
    model = Sitemap
    fields = (
      # 'statics',
      'categories',
      'products',
      'posts',
    )

  def to_representation(self, instance):
    representation = super().to_representation(instance)

    return {
      'categories': representation['categories'],
      'products': representation['products'],
      'posts': representation['posts'],
    }