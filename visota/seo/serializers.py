from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

from .models import *


class SEOStaticPageSerializer(TranslatableModelSerializer):

  class Meta:
    model = SEOStaticPage
    fields = (
      'header',
      'title',
      'description',
      'noindex_follow',
    )

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


class SitemapStaticsSerializer(TranslatableModelSerializer):
  translations = TranslatedFieldsField(shared_model=SEOStaticPage)
  
  class Meta:
    model = SEOStaticPage
    fields = (
      'page',
      'translations',
    )

  def to_representation(self, instance):
    represention = super().to_representation(instance)
    translations = represention['translations']
    result = {
      'page': represention['page'],
      'langs': {}
    }
    for key in translations:
      result['langs'][key] = {}
      result['langs'][key]['priority'] = translations.get(key, None)['priority'] if translations.get(key, None) else None
      result['langs'][key]['changeFrequency'] = translations.get(key, None)['change_freq'] if translations.get(key, None) else None
    return result




class CategorySlugSerializer(TranslatableModelSerializer):
  translations = TranslatedFieldsField(shared_model=SubCategory)

  class Meta:
    model = SubCategory
    fields = (
      'translations',
    )


class SEOCategoryPageSerializer(TranslatableModelSerializer):
  category = CategorySlugSerializer()

  class Meta:
    model = SEOCategoryPage
    fields = (
      'category',
      'title',
      'description',
      'noindex_follow',
    )

  def to_representation(self, instance):
    translated = instance.has_translation(instance.get_current_language())

    if translated:
      representation = super().to_representation(instance)
      
      translations = representation['category']['translations']
      slug = {}
      for key in translations:
        slug[key] = translations[key]['slug']

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
        'meta': meta,
        'slug': slug
      }
      
    else:
      result = {'translated': False}
    
    return result


class SitemapCategoriesSerializer(TranslatableModelSerializer):
  category = CategorySlugSerializer()
  translations = TranslatedFieldsField(shared_model=SEOCategoryPage)

  class Meta:
    model = SEOCategoryPage
    fields = (
      'category',
      'translations',
    )

  def to_representation(self, instance):
    represention = super().to_representation(instance)
    translations = represention['category']['translations']
    seo_translations = represention['translations']
    result = {}
    for key in translations:
      result[key] = {}
      result[key]['slug'] = translations[key]['slug']
      result[key]['lastModified'] = translations[key]['last_modified']
      result[key]['priority'] = seo_translations.get(key, None)['priority'] if seo_translations.get(key, None) else None
      result[key]['changeFrequency'] = seo_translations.get(key, None)['change_freq'] if seo_translations.get(key, None) else None
    return result
  



class TagSlugSerializer(TranslatableModelSerializer):
  translations = TranslatedFieldsField(shared_model=Tag)

  class Meta:
    model = Tag
    fields = (
      'translations',
    )


class SEOTagPageSerializer(TranslatableModelSerializer):
  tag = TagSlugSerializer()

  class Meta:
    model = SEOTagPage
    fields = (
      'tag',
      'title',
      'description',
      'noindex_follow',
    )

  def to_representation(self, instance):
    translated = instance.has_translation(instance.get_current_language())

    if translated:
      representation = super().to_representation(instance)
      
      translations = representation['tag']['translations']
      slug = {}
      for key in translations:
        slug[key] = translations[key]['slug']

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
        'meta': meta,
        'slug': slug
      }
      
    else:
      result = {'translated': False}
    
    return result


class SitemapTagSerializer(TranslatableModelSerializer):
  tag = TagSlugSerializer()
  translations = TranslatedFieldsField(shared_model=SEOTagPage)

  class Meta:
    model = SEOTagPage
    fields = (
      'tag',
      'translations',
    )

  def to_representation(self, instance):
    represention = super().to_representation(instance)
    translations = represention['tag']['translations']
    seo_translations = represention['translations']
    result = {}
    for key in translations:
      result[key] = {}
      result[key]['slug'] = translations[key]['slug']
      result[key]['lastModified'] = translations[key]['last_modified']
      result[key]['priority'] = seo_translations.get(key, None)['priority'] if seo_translations.get(key, None) else None
      result[key]['changeFrequency'] = seo_translations.get(key, None)['change_freq'] if seo_translations.get(key, None) else None
    return result




class ProductSlugSerializer(TranslatableModelSerializer):
  translations = TranslatedFieldsField(shared_model=Product)

  class Meta:
    model = Product
    fields = (
      'translations',
    )


class SEOProductPageSerializer(TranslatableModelSerializer):
  product = ProductSlugSerializer()

  class Meta:
    model = SEOProductPage
    fields = (
      'product',
      'title',
      'description',
      'noindex_follow',
    )

  def to_representation(self, instance):
    translated = instance.has_translation(instance.get_current_language())

    if translated:
      representation = super().to_representation(instance)
      
      translations = representation['product']['translations']
      slug = {}
      for key in translations:
        slug[key] = translations[key]['slug']

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
        'meta': meta,
        'slug': slug
      }
      
    else:
      result = {'translated': False}
    
    return result


class SitemapProductsSerializer(TranslatableModelSerializer):
  product = ProductSlugSerializer()
  translations = TranslatedFieldsField(shared_model=SEOProductPage)

  class Meta:
    model = SEOProductPage
    fields = (
      'product',
      'translations'
    )

  def to_representation(self, instance):
    represention = super().to_representation(instance)
    translations = represention['product']['translations']
    seo_translations = represention['translations']
    result = {}
    for key in translations:
      result[key] = {}
      result[key]['slug'] = translations[key]['slug']
      result[key]['lastModified'] = translations[key]['last_modified']
      result[key]['priority'] = seo_translations.get(key, None)['priority'] if seo_translations.get(key, None) else None
      result[key]['changeFrequency'] = seo_translations.get(key, None)['change_freq'] if seo_translations.get(key, None) else None
    return result




class PostSlugSerializer(TranslatableModelSerializer):
  translations = TranslatedFieldsField(shared_model=Post)

  class Meta:
    model = Post
    fields = (
      'translations',
    )


class SEOPostPageSerializer(TranslatableModelSerializer):
  post = PostSlugSerializer()

  class Meta:
    model = SEOProductPage
    fields = (
      'post',
      'title',
      'description',
      'noindex_follow',
    )

  def to_representation(self, instance):
    translated = instance.has_translation(instance.get_current_language())

    if translated:
      representation = super().to_representation(instance)
      
      translations = representation['post']['translations']
      slug = {}
      for key in translations:
        slug[key] = translations[key]['slug']

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
        'meta': meta,
        'slug': slug
      }
      
    else:
      result = {'translated': False}
    
    return result


class SitemapPostsSerializer(TranslatableModelSerializer):
  post = PostSlugSerializer()
  translations = TranslatedFieldsField(shared_model=SEOPostPage)

  class Meta:
    model = SEOPostPage
    fields = (
      'post',
      'translations'
    )

  def to_representation(self, instance):
    represention = super().to_representation(instance)
    translations = represention['post']['translations']
    seo_translations = represention['translations']
    result = {}
    for key in translations:
      result[key] = {}
      result[key]['slug'] = translations[key]['slug']
      result[key]['lastModified'] = translations[key]['last_modified']
      result[key]['priority'] = seo_translations.get(key, None)['priority'] if seo_translations.get(key, None) else None
      result[key]['changeFrequency'] = seo_translations.get(key, None)['change_freq'] if seo_translations.get(key, None) else None
    return result




class SitemapSerializer(serializers.ModelSerializer):
  statics = SitemapStaticsSerializer(many=True)
  categories = SitemapCategoriesSerializer(many=True)
  tags = SitemapTagSerializer(many=True)
  products = SitemapProductsSerializer(many=True)
  posts = SitemapPostsSerializer(many=True)


  class Meta:
    model = Sitemap
    fields = (
      'statics',
      'categories',
      'tags',
      'products',
      'posts',
    )

  def to_representation(self, instance):
    representation = super().to_representation(instance)

    return {
      'statics': representation['statics'],
      'categories': representation['categories'],
      'tags': representation['tags'],
      'products': representation['products'],
      'posts': representation['posts'],
    }