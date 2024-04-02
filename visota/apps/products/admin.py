from django.contrib import admin
from django import forms

# Register your models here.
from .models import Product, Category, SubCategory, Charachteristic, CharValue, ProductImg

# Register your models here.
class ImgInline(admin.TabularInline):
    model = ProductImg
    min_num = 1


class ProductAdminForm(forms.ModelForm):
    # charachteristics = forms.ModelMultipleChoiceField(queryset=CharValue.objects.order_by('char__name'))
    # sub_categories = forms.ModelMultipleChoiceField(queryset=SubCategory.objects.order_by('name'))

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['charachteristics'].queryset = (
            self.fields['charachteristics'].queryset.order_by('char__name')
        )
        self.fields['sub_categories'].queryset = (
            self.fields['sub_categories'].queryset.order_by('name')
        )


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", 'code')}
    list_display = ["name", "code", 'actual_price', 'current_price']
    inlines = [ImgInline,]
    form = ProductAdminForm


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name",]


class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", 'category']




admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register([Charachteristic, CharValue])