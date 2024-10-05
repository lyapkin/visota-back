from django.contrib import admin
from django import forms
from django.http import HttpRequest
from parler.admin import TranslatableAdmin, TranslatableTabularInline, SortedRelatedFieldListFilter
from parler.forms import TranslatableModelForm

# Register your models here.
from .models import Product, Category, SubCategory, CharValue, ProductImg, CategoryRedirectFrom, ProductRedirectFrom, Tag, TagRedirectFrom, Filter
from .signals import full_product_save_admin, full_category_save_admin

# Register your models here.


class ImgInline(admin.TabularInline):
    model = ProductImg
    min_num = 1

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        return formset
    

class CharachterInline(TranslatableTabularInline):
    model = CharValue
    # def get_formset(self, request, obj=None, **kwargs):
    #     formset = super().get_formset(request, obj=None, **kwargs)
    #     formset.validate_min = True
    #     return formset


# class DocInline(admin.TabularInline):
#     model = ProductDoc


# class ProductAdminForm(TranslatableModelForm):
#     # charachteristics = forms.ModelMultipleChoiceField(queryset=CharValue.objects.order_by('char__name'))
#     # sub_categories = forms.ModelMultipleChoiceField(queryset=SubCategory.objects.order_by('name'))

#     class Meta:
#         model = Product
#         exclude = ('slug',)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['charachteristics'].queryset = (
#             self.fields['charachteristics'].queryset.order_by('char__name')
#         )
#         self.fields['sub_categories'].queryset = (
#             self.fields['sub_categories'].queryset.order_by('name')
#         )


class ProductRedirectFromInline(admin.TabularInline):
  model = ProductRedirectFrom
  extra = 1

class ProductAdmin(TranslatableAdmin):
    fields = ['name', 'slug', 'sub_categories', 'tags', 'code', 'actual_price', 'current_price', 'is_present', 'description', 'filters', 'priority']
    list_display = ["name", "code", 'actual_price', 'current_price']
    inlines = [CharachterInline, ImgInline, ProductRedirectFromInline]
    # inlines = [CharachterInline, ImgInline, DocInline]
    # form = ProductAdminForm
    filter_horizontal = ("sub_categories", "tags", "filters")

    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return super(ProductAdmin, self).get_queryset(request).translated(language_code)
    
    # def save_related(self, request, form, formsets, change):
    #   super().save_related(request, form, formsets, change)
    #   changed = form.has_changed()
    #   for f in formsets:
    #     if f.model is CharValue:
    #       changed = changed or f.has_changed()
    #   receivers = full_product_save_admin.send(sender=Product, instance=form.instance, changed=changed)


class CategoryAdmin(TranslatableAdmin):
    list_display = ["name",]
    exclude = ('slug',)

    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return super(CategoryAdmin, self).get_queryset(request).translated(language_code).order_by('translations__name')
    
    def has_add_permission(self, request, obj=None):
      return False
    
    def has_delete_permission(self, request, obj=None):
      return False


class CategoryRedirectFromInline(admin.TabularInline):
  model = CategoryRedirectFrom
  extra = 1

class SubCategoryAdmin(TranslatableAdmin):
    fields = ['name', 'slug', 'category', 'filters', 'img', 'description', 'priority']
    list_display = ["name", 'category']
    inlines = (CategoryRedirectFromInline,)
    filter_horizontal = ("filters",)

    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return super(SubCategoryAdmin, self).get_queryset(request).translated(language_code).order_by('translations__name')

    # def save_related(self, request, form, formsets, change):
    #   super().save_related(request, form, formsets, change)
    #   changed = False
    #   for d in form.changed_data:
    #     if d == 'name' or d == 'description':
    #        changed = True
    #   receivers = full_category_save_admin.send(sender=SubCategory, instance=form.instance, changed=changed)


class TagRedirectFromInline(admin.TabularInline):
  model = TagRedirectFrom
  extra = 1

class TagAdmin(TranslatableAdmin):
    fields = ['name', 'slug']
    list_display = ["name"]
    inlines = (TagRedirectFromInline,)

    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return super(TagAdmin, self).get_queryset(request).translated(language_code).order_by('translations__name')

    # def save_related(self, request, form, formsets, change):
    #   super().save_related(request, form, formsets, change)
    #   changed = False
    #   for d in form.changed_data:
    #     if d == 'name':
    #        changed = True
    #   receivers = full_tag_save_admin.send(sender=Tag, instance=form.instance, changed=changed)


class FilterAdmin(TranslatableAdmin):
    fields = ['name', 'slug']
    list_display = ["name"]

    # def get_queryset(self, request):
    #     # Limit to a single language!
    #     language_code = self.get_queryset_language(request)
    #     return super(TagAdmin, self).get_queryset(request).translated(language_code).order_by('translations__name')


class CharValueAdmin(TranslatableAdmin):
    list_display = ['product', 'key', 'value']
    # fields = ['value']

    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return super(CharValueAdmin, self).get_queryset(request).translated(language_code).order_by('product')



admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(CharValue, CharValueAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Filter, FilterAdmin)
# admin.site.register(CharValue)