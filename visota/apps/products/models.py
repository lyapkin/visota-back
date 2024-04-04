from django.db import models

from common.utils import upload_product_img_to

# Create your models here.
class Category(models.Model):
    name = models.CharField("название категории", max_length=50, unique=True)
    slug = models.SlugField("url", max_length=60, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class SubCategory(models.Model):
    name = models.CharField("название подкатегории", max_length=50, unique=True)
    slug = models.SlugField("url", max_length=60, unique=True)
    category = models.ForeignKey(Category, models.CASCADE, related_name='subcategories', verbose_name='категория')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "подкатегория"
        verbose_name_plural = "подкатегории"


class Charachteristic(models.Model):
    name = models.CharField("название характеристики", max_length=30, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "характеристика товара"
        verbose_name_plural = "характеристики товаров"


class CharValue(models.Model):
    char = models.ForeignKey(Charachteristic, models.CASCADE, related_name='values', verbose_name='название характеристики товара')
    value = models.CharField("значение характеристики", max_length=50, unique=True)

    def __str__(self):
        return self.char.name + ' ' + self.value
    
    class Meta:
        verbose_name = "значение характеристики товара"
        verbose_name_plural = "значения характеристик товара"


class Product(models.Model):
    name = models.CharField("название товара", max_length=100)
    code = models.CharField("артикул", max_length=20, unique=True)
    slug = models.SlugField("url", max_length=130, unique=True)
    sub_categories = models.ManyToManyField(SubCategory, related_name='products', verbose_name='подкатегория товара')
    actual_price = models.PositiveIntegerField('цена')
    current_price = models.PositiveIntegerField('текущая цена (со скидкой)')
    charachteristics = models.ManyToManyField(CharValue, verbose_name='характеристики товара')
    description = models.TextField('описание товара')
    is_present = models.BooleanField('в наличии', default=False)

    def __str__(self):
        return self.name + ' ' + self.code
    
    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"


class ProductImg(models.Model):
    img_url = models.ImageField("изображение товара", upload_to=upload_product_img_to)
    product = models.ForeignKey(Product, models.CASCADE, related_name='img_urls', verbose_name='товар')

    def __str__(self):
        return str(self.img_url)
    
    class Meta:
        verbose_name = "изображение товара"
        verbose_name_plural = "изображения товара"