from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from parler.admin import TranslatableAdmin
from .models import *

# Register your models here.
class RobotsAdmin(admin.ModelAdmin):
  def has_add_permission(self, request, obj=None):
    return False
    
  def has_delete_permission(self, request, obj=None):
    return False
  
admin.site.register(Robots, RobotsAdmin)


class SEOStaticPageAdmin(TranslatableAdmin):
  ordering = ('order',)

  def get_fieldsets(self, request, obj=None):
    if obj:
      return (
        (None, {
           'fields': ['name', 'header', 'title', 'description', 'noindex_follow', 'order']
        }),
        ('Sitemap', {
            'fields': ('change_freq', 'priority'),
        }),
      )
    else:
      return (
        (None, {
           'fields': ['page', 'name', 'header', 'title', 'description', 'noindex_follow', 'order']
        }),
        ('Sitemap', {
            'fields': ('change_freq', 'priority'),
        }),
      )

  # def get_fields(self, request, obj=None):
  #   if obj:
  #       return ['name', 'header', 'title', 'description', 'noindex_follow', 'order', 'change_freq', 'priority']
  #   else:
  #       return ['page', 'name', 'header', 'title', 'description', 'noindex_follow', 'order', 'change_freq', 'priority']

  def get_readonly_fields(self, request, obj=None):
    if obj:
        return ["name"]
    else:
        return []
    
  def has_add_permission(self, request, obj=None):
    return False
    
  def has_delete_permission(self, request, obj=None):
    return False

admin.site.register(SEOStaticPage, SEOStaticPageAdmin)


class SEOCategoryPageAdmin(TranslatableAdmin):
  fieldsets = (
    (None, {
        'fields': ['category', 'title', 'description', 'noindex_follow']
    }),
    ('Sitemap', {
        'fields': ('change_freq', 'priority'),
    }),
  )

  def get_readonly_fields(self, request, obj=None):
    if obj:
        return ["category"]
    else:
        return []
    
admin.site.register(SEOCategoryPage, SEOCategoryPageAdmin)


class SEOProductPageAdmin(TranslatableAdmin):
  fieldsets = (
    (None, {
        'fields': ['product', 'title', 'description', 'noindex_follow']
    }),
    ('Sitemap', {
        'fields': ('change_freq', 'priority'),
    }),
  )

  def get_readonly_fields(self, request, obj=None):
    if obj:
        return ["product"]
    else:
        return []
    
admin.site.register(SEOProductPage, SEOProductPageAdmin)


class SEOPostPageAdmin(TranslatableAdmin):
  fieldsets = (
    (None, {
        'fields': ['post', 'title', 'description', 'noindex_follow']
    }),
    ('Sitemap', {
        'fields': ('change_freq', 'priority'),
    }),
  )

  def get_readonly_fields(self, request, obj=None):
    if obj:
        return ["post"]
    else:
        return []
    
admin.site.register(SEOPostPage, SEOPostPageAdmin)