from django.contrib import admin
from django import forms
from parler.admin import TranslatableAdmin, TranslatableTabularInline, SortedRelatedFieldListFilter
from parler.forms import TranslatableModelForm

# Register your models here.
from .models import Product, Category, SubCategory, CharValue, ProductImg

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


class ProductAdmin(TranslatableAdmin):
    list_display = ["name", "code", 'actual_price', 'current_price']
    inlines = [CharachterInline, ImgInline]
    exclude = ('slug',)
    # inlines = [CharachterInline, ImgInline, DocInline]
    # form = ProductAdminForm
    filter_horizontal = ("sub_categories",)

    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return super(ProductAdmin, self).get_queryset(request).translated(language_code)


class CategoryAdmin(TranslatableAdmin):
    list_display = ["name",]
    exclude = ('slug',)

    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return super(CategoryAdmin, self).get_queryset(request).translated(language_code).order_by('translations__name')


class SubCategoryAdmin(TranslatableAdmin):
    list_display = ["name", 'category']

    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return super(SubCategoryAdmin, self).get_queryset(request).translated(language_code).order_by('translations__name')



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
# admin.site.register(CharValue)