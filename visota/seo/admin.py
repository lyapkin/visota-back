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
  actions = ['generate_meta']

  def get_readonly_fields(self, request, obj=None):
    if obj:
        return ["category"]
    else:
        return []
    
  @admin.action(description="Сгенерировать метаданные")
  def generate_meta(self, request, queryset):
      rule = MetaGenerationRule.objects.get(type='ctg')
      for seo in queryset:
        category = seo.category
        for translation in category.translations.all():
          if rule.has_translation(translation.language_code):
            rule.set_current_language(translation.language_code)
            title = rule.title.format(name=translation.name, description=translation.description)
            description = rule.description.format(name=translation.name, description=translation.description)
          else:
            title = translation.name
            description = translation.description
          seo.set_current_language(translation.language_code)
          seo.title = title
          seo.description = description
        seo.save()
    
admin.site.register(SEOCategoryPage, SEOCategoryPageAdmin)


class SEOTagPageAdmin(TranslatableAdmin):
  fieldsets = (
    (None, {
        'fields': ['tag', 'title', 'description', 'noindex_follow']
    }),
    ('Sitemap', {
        'fields': ('change_freq', 'priority'),
    }),
  )
  actions = ['generate_meta']

  def get_readonly_fields(self, request, obj=None):
    if obj:
        return ["tag"]
    else:
        return []
    
  @admin.action(description="Сгенерировать метаданные")
  def generate_meta(self, request, queryset):
      rule = MetaGenerationRule.objects.get(type='tag')
      for seo in queryset:
        tag = seo.tag
        for translation in tag.translations.all():
          if rule.has_translation(translation.language_code):
            rule.set_current_language(translation.language_code)
            title = rule.title.format(name=translation.name)
            description = rule.description.format(name=translation.name)
          else:
            title = translation.name
            description = translation.name
          seo.set_current_language(translation.language_code)
          seo.title = title
          seo.description = description
        seo.save()
    
admin.site.register(SEOTagPage, SEOTagPageAdmin)


class SEOProductPageAdmin(TranslatableAdmin):
  fieldsets = (
    (None, {
        'fields': ['product', 'title', 'description', 'noindex_follow']
    }),
    ('Sitemap', {
        'fields': ('change_freq', 'priority'),
    }),
  )
  actions = ['generate_meta']

  def get_readonly_fields(self, request, obj=None):
    if obj:
        return ["product"]
    else:
        return []
    
  @admin.action(description="Сгенерировать метаданные")
  def generate_meta(self, request, queryset):
      rule = MetaGenerationRule.objects.get(type='prd')
      for seo in queryset:
        product = seo.product
        for translation in product.translations.all():
          lang = translation.language_code
          if rule.has_translation(lang):
            rule.set_current_language(lang)

            price = product.current_price or product.actual_price or ''
            cats_q = product.sub_categories.language(lang).filter(translations__language_code=lang)
            cats = ', '.join([c.name for c in cats_q])
            chars_q = product.charachteristics.language(lang).filter(translations__language_code=lang)
            chars = '; '.join(['{} - {}'.format(char.key, char.value) for char in chars_q])

            title = rule.title.format(name=translation.name, price=price, cats=cats, chars=chars)
            description = rule.description.format(name=translation.name, price=price, cats=cats, chars=chars)
          else:
            title = translation.name
            description = translation.name
          seo.set_current_language(lang)
          seo.title = title
          seo.description = description
        seo.save()
    
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


class MetaGenerationRuleAdmin(TranslatableAdmin):
  fields = ['type', 'instruction', 'title', 'description']
  def get_readonly_fields(self, request, obj=None):
    if obj:
        return ["type", "instruction"]
    else:
        return []
    
  def has_add_permission(self, request, obj=None):
    return False
    
  def has_delete_permission(self, request, obj=None):
    return False
    
    
admin.site.register(MetaGenerationRule, MetaGenerationRuleAdmin)


class JSFileAdmin(admin.ModelAdmin):
  def get_readonly_fields(self, request, obj=None):
    if obj:
        return ["name"]
    else:
        return []
    
  def has_add_permission(self, request, obj=None):
    return False
    
  def has_delete_permission(self, request, obj=None):
    return False
    
    
admin.site.register(JSFile, JSFileAdmin)


class CSSFileAdmin(admin.ModelAdmin):
  def get_readonly_fields(self, request, obj=None):
    if obj:
        return ["name"]
    else:
        return []
    
  def has_add_permission(self, request, obj=None):
    return False
    
  def has_delete_permission(self, request, obj=None):
    return False
    
    
admin.site.register(CSSFile, CSSFileAdmin)