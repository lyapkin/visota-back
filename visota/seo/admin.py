from django.contrib import admin
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

  def get_fields(self, request, obj=None):
    if obj:
        return ['name', 'header', 'title', 'description', 'noindex_follow']
    else:
        return ['page', 'name', 'header', 'title', 'description', 'noindex_follow']

  def get_readonly_fields(self, request, obj=None):
    if obj:
        return ["name"]
    else:
        return []

admin.site.register(SEOStaticPage, SEOStaticPageAdmin)