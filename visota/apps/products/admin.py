from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.translation import get_language
from parler.admin import (
    TranslatableAdmin,
    TranslatableTabularInline,
    TranslatableBaseInlineFormSet,
)

# Register your models here.
from .models import (
    Product,
    Category,
    SubCategory,
    ProductImg,
    CategoryRedirectFrom,
    ProductRedirectFrom,
    Tag,
    TagRedirectFrom,
    ProductCharacteristic,
    Characteristic,
    CharacteristicValue,
)
from .signals import full_product_save_admin, full_category_save_admin

# Register your models here.


class ImgInline(admin.TabularInline):
    model = ProductImg
    min_num = 1

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        return formset


# class DocInline(admin.TabularInline):
#     model = ProductDoc


class CharacteristicInline(admin.TabularInline):
    model = ProductCharacteristic

    def get_formset(self, request, obj=None, **kwargs):
        fs = super().get_formset(request, obj, **kwargs)
        fs.form.base_fields["characteristic_value"].widget.can_add_related = False
        fs.form.base_fields["characteristic_value"].widget.can_change_related = False
        fs.form.base_fields["characteristic_value"].widget.can_view_related = False
        # fs.form.base_fields['some_field'].widget.can_delete_related = False

        language_code = get_language()
        fs.form.base_fields["characteristic"].queryset = Characteristic.objects.translated(language_code).order_by(
            "translations__name"
        )

        return fs


class ProductRedirectFromInline(admin.TabularInline):
    model = ProductRedirectFrom
    extra = 1


class ProductAdmin(TranslatableAdmin):
    fields = [
        "name",
        "slug",
        "sub_categories",
        "tags",
        "code",
        "actual_price",
        "current_price",
        "is_present",
        "description",
        "priority",
    ]
    list_display = ["name", "code", "actual_price", "current_price"]
    inlines = [
        CharacteristicInline,
        ImgInline,
        ProductRedirectFromInline,
    ]
    # inlines = [CharachterInline, ImgInline, DocInline]
    # form = ProductAdminForm
    filter_horizontal = (
        "sub_categories",
        "tags",
    )

    # def save_related(self, request, form, formsets, change):
    #   super().save_related(request, form, formsets, change)
    #   changed = form.has_changed()
    #   for f in formsets:
    #     if f.model is CharValue:
    #       changed = changed or f.has_changed()
    #   receivers = full_product_save_admin.send(sender=Product, instance=form.instance, changed=changed)


class CategoryAdmin(TranslatableAdmin):
    list_display = [
        "name",
    ]
    exclude = ("slug",)

    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return (
            super(CategoryAdmin, self).get_queryset(request).translated(language_code).order_by("translations__name")
        )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CategoryRedirectFromInline(admin.TabularInline):
    model = CategoryRedirectFrom
    extra = 1


class SubCategoryAdmin(TranslatableAdmin):
    fields = ["name", "slug", "category", "img", "description", "priority"]
    list_display = ["name", "category"]
    inlines = (CategoryRedirectFromInline,)

    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return (
            super(SubCategoryAdmin, self)
            .get_queryset(request)
            .translated(language_code)
            .order_by("translations__name")
        )

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
    fields = ["name", "slug"]
    list_display = ["name"]
    inlines = (TagRedirectFromInline,)

    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return super(TagAdmin, self).get_queryset(request).translated(language_code).order_by("translations__name")

    # def save_related(self, request, form, formsets, change):
    #   super().save_related(request, form, formsets, change)
    #   changed = False
    #   for d in form.changed_data:
    #     if d == 'name':
    #        changed = True
    #   receivers = full_tag_save_admin.send(sender=Tag, instance=form.instance, changed=changed)


class CharacteristicValueInlineFormSet(TranslatableBaseInlineFormSet):
    def validate_unique(self):
        name_values = set()
        slug_values = set()
        errors = []
        for form in self.forms:
            name = form["name"].value().strip()
            slug = form["slug"].value().strip()

            if name == "":
                continue

            if name in name_values:
                errors.append("Задано несколько одинаковых значений")
            else:
                name_values.add(name)

            if slug == "":
                continue

            if slug in slug_values:
                errors.append("Задано несколько одинаковых слагов")
            else:
                slug_values.add(slug)

        if errors:
            raise ValidationError(errors)

        return super().validate_unique()


class CharacteristicValueInline(TranslatableTabularInline):
    model = CharacteristicValue
    formset = CharacteristicValueInlineFormSet

    verbose_name = "Возможное значение характеристики"
    verbose_name_plural = "Возможные значения характеристики"


class CharachteristicAdmin(TranslatableAdmin):
    inlines = (CharacteristicValueInline,)

    def get_queryset(self, request):
        language_code = self.get_queryset_language(request)
        return super().get_queryset(request).translated(language_code).order_by("translations__name")


admin.site.register(Characteristic, CharachteristicAdmin)


class CharachteristicValueAdmin(TranslatableAdmin):
    def get_model_perms(self, request):
        return {}


admin.site.register(CharacteristicValue, CharachteristicValueAdmin)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Tag, TagAdmin)
