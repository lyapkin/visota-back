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