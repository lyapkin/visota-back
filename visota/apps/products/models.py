from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from parler.models import TranslatableModel, TranslatedFields
from common.utils import generate_unique_slug, generate_unique_slug_translated, upload_category_img_to, upload_group_img_to


from common.utils import upload_product_img_to, upload_product_file_to

# Create your models here.
class Category(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField("название категории", max_length=50, unique=True)
    )
    slug = models.SlugField("url", max_length=60, unique=True)
    priority = models.PositiveSmallIntegerField('позиция в фильтре каталога', default=32000)
    img = models.ImageField("картинка группы", upload_to=upload_group_img_to, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        # ordering = ('translations__name',)

    def save(self, *args, **kwargs):
        if not self.slug.strip():
            self.slug = generate_unique_slug(Category, self.name)
        return super().save(*args, **kwargs)


class SubCategory(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField("название подкатегории", max_length=50, unique=True)
    )
    slug = models.SlugField("url", max_length=60, unique=True)
    category = models.ForeignKey(Category, models.CASCADE, related_name='subcategories', verbose_name='категория')
    priority = models.PositiveSmallIntegerField('позиция в фильтре каталога', default=32000)
    img = models.ImageField("картинка категории", upload_to=upload_category_img_to, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "подкатегория"
        verbose_name_plural = "подкатегории"
        # ordering = ('translations__name',)

    def save(self, *args, **kwargs):
        if not self.slug.strip():
            self.slug = generate_unique_slug(SubCategory, self.name)
        return super().save(*args, **kwargs)


class Product(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField("название товара", max_length=100, unique=True),
        slug = models.SlugField("url", max_length=130, unique=True),
        description = CKEditor5Field("описание товара", config_name='extends'),
        priority = models.PositiveSmallIntegerField('позиция в выдаче', default=32000)
    )
    code = models.CharField("артикул", max_length=20, unique=True, null=True, blank=True)
    sub_categories = models.ManyToManyField(SubCategory, related_name='products', verbose_name='подкатегория товара')
    actual_price = models.PositiveIntegerField('цена', null=True, blank=True)
    current_price = models.PositiveIntegerField('текущая цена (со скидкой)', null=True, blank=True)
    # description = models.TextField('описание товара')
    is_present = models.BooleanField('в наличии', default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        # ordering = ('translations__name',)

    def save(self, *args, **kwargs):
        if not self.slug.strip():
            self.slug = generate_unique_slug_translated(Product, self.name)
        return super().save(*args, **kwargs)


class CharValue(TranslatableModel):
    translations = TranslatedFields(
        key = models.CharField('характеристика', max_length=50),
        value = models.CharField("значение характеристики", max_length=50),
        # meta = {'unique_together': [('key', 'value','product')]}
    )
    product = models.ForeignKey(Product, models.CASCADE, related_name='charachteristics', verbose_name='товар')

    def __str__(self):
        return self.product.name + ' ' + self.key + ' ' + self.value
    
    class Meta:
        verbose_name = "характеристика товара"
        verbose_name_plural = "характеристики товаров"
        # unique_together = ['translations', 'product']


class ProductImg(models.Model):
    img_url = models.ImageField("изображение товара", upload_to=upload_product_img_to)
    product = models.ForeignKey(Product, models.CASCADE, related_name='img_urls', verbose_name='товар')

    def __str__(self):
        return str(self.img_url)
    
    class Meta:
        verbose_name = "изображение товара"
        verbose_name_plural = "изображения товара"


# class ProductDoc(models.Model):
#     file_name = models.CharField('Название документа', max_length=100)
#     doc_url = models.FileField("документ", upload_to=upload_product_file_to)
#     product = models.ForeignKey(Product, models.CASCADE, related_name='doc_urls', verbose_name='товар')

#     def __str__(self):
#         return str(self.file_name + ' ' + str(self.id))
    
#     class Meta:
#         verbose_name = "документ товара"
#         verbose_name_plural = "документы товара"   