from datetime import date
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from parler.models import TranslatableModel, TranslatedFields
from common.utils import generate_unique_slug, generate_unique_slug_translated, upload_category_img_to, upload_group_img_to


from common.utils import upload_product_img_to, upload_product_file_to

# Create your models here.
class CategoryRedirectFrom(models.Model):
  to = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
  old_slug = models.CharField("старый url", max_length=60, unique=True)
  lang = models.CharField('языковая версия категории старого url', max_length=2, choices=settings.LANGUAGES, default='ru')

  # class Meta:
  #   constraints = [
  #     models.UniqueConstraint(fields=['old_slug', 'lang'], name='unique_slug_for_lang'),
  #   ]

  def __str__(self):
    category = self.to
    category.set_current_language('ru')
    return f'язык: {self.lang}; старый слаг: {self.old_slug}; к: {category.name}'
    
  class Meta:
    verbose_name = "Старый слаг (редирект (seo))"
    verbose_name_plural = "Старые слаги (редирект (seo))"


class ProductRedirectFrom(models.Model):
  to = models.ForeignKey('Product', on_delete=models.CASCADE)
  old_slug = models.CharField("старый url", max_length=60, unique=True)
  lang = models.CharField('языковая версия продукта старого url', max_length=2, choices=settings.LANGUAGES, default='ru')

  def __str__(self):
    product = self.to
    product.set_current_language('ru')
    return f'язык: {self.lang}; старый слаг: {self.old_slug}; к: {product.name}'
    
  class Meta:
    verbose_name = "Старый слаг (редирект (seo))"
    verbose_name_plural = "Старые слаги (редирект (seo))"


class TagRedirectFrom(models.Model):
  to = models.ForeignKey('Tag', on_delete=models.CASCADE)
  old_slug = models.CharField("старый url", max_length=60, unique=True)
  lang = models.CharField('языковая версия тега старого url', max_length=2, choices=settings.LANGUAGES, default='ru')

  def __str__(self):
    tag = self.to
    tag.set_current_language('ru')
    return f'язык: {self.lang}; старый слаг: {self.old_slug}; к: {tag.name}'
    
  class Meta:
    verbose_name = "Старый слаг (редирект (seo))"
    verbose_name_plural = "Старые слаги (редирект (seo))"


class Filter(TranslatableModel):
  translations = TranslatedFields(
     name = models.CharField("название фильтра", max_length=50, unique=True),
     slug = models.SlugField("slug", max_length=60, unique=True, blank=True),
  )

  def __str__(self):
    return self.name
    
  class Meta:
    verbose_name = "фильтр"
    verbose_name_plural = "фильтры"

  def save(self, *args, **kwargs):
    if not self.slug.strip():
      self.slug = generate_unique_slug_translated(Filter, None, self.name)
    return super().save(*args, **kwargs)


class Category(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField("название группы", max_length=50, unique=True)
    )
    slug = models.SlugField("url", max_length=60, unique=True)
    priority = models.PositiveSmallIntegerField('позиция в фильтре каталога', default=32000)
    img = models.ImageField("картинка группы", upload_to=upload_group_img_to, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "группа категории"
        verbose_name_plural = "группы категорий"

    def save(self, *args, **kwargs):
        if not self.slug.strip():
            self.slug = generate_unique_slug(Category, self.name)
        return super().save(*args, **kwargs)
    

def validate_is_category_slug_old(value):
  result = CategoryRedirectFrom.objects.filter(old_slug=value).exists()
  if result:
      raise ValidationError('Этот slug уже использовался')


class SubCategory(TranslatableModel):
    translations = TranslatedFields(
      name = models.CharField("название категории", max_length=50, unique=True),
      slug = models.SlugField("url", max_length=60, unique=True, blank=True, validators=[validate_is_category_slug_old]),
      description = models.TextField('описание'),
      last_modified = models.DateField(auto_now=True)
    )
    category = models.ForeignKey(Category, models.CASCADE, related_name='subcategories', verbose_name='группа')
    priority = models.PositiveSmallIntegerField('позиция в фильтре каталога', default=32000)
    img = models.ImageField("картинка категории", upload_to=upload_category_img_to, null=True)

    filters = models.ManyToManyField(Filter, related_name='categories', verbose_name='фильтры')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def save(self, *args, **kwargs):
        if not self.slug.strip():
            self.slug = generate_unique_slug_translated(SubCategory, SubCategory.categoryredirectfrom_set.rel.related_model, self.name)
        return super().save(*args, **kwargs)
    

def validate_is_tag_slug_old(value):
  result = TagRedirectFrom.objects.filter(old_slug=value).exists()
  if result:
      raise ValidationError('Этот slug уже использовался')


class Tag(TranslatableModel):
    translations = TranslatedFields(
      name = models.CharField("название тега", max_length=50, unique=True),
      slug = models.SlugField("url", max_length=60, unique=True, blank=True, validators=[validate_is_tag_slug_old]),
      last_modified = models.DateField(auto_now=True)
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def save(self, *args, **kwargs):
        if not self.slug.strip():
            self.slug = generate_unique_slug_translated(Tag, Tag.tagredirectfrom_set.rel.related_model, self.name)
        return super().save(*args, **kwargs)


def validate_is_product_slug_old(value):
  result = ProductRedirectFrom.objects.filter(old_slug=value).exists()
  if result:
      raise ValidationError('Этот slug уже использовался')


class Product(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField("название товара", max_length=100, unique=True),
        slug = models.SlugField("url", max_length=130, unique=True, blank=True, validators=[validate_is_product_slug_old]),
        description = CKEditor5Field("описание товара", config_name='extends'),
        priority = models.PositiveSmallIntegerField('позиция в выдаче', default=32000),
        last_modified = models.DateField(auto_now=True)
    )
    code = models.CharField("артикул", max_length=20, unique=True, null=True, blank=True)
    sub_categories = models.ManyToManyField(SubCategory, related_name='products', verbose_name='категория товара')
    tags = models.ManyToManyField(Tag, related_name='products', verbose_name='теги', blank=True)
    actual_price = models.PositiveIntegerField('цена', null=True, blank=True)
    current_price = models.PositiveIntegerField('текущая цена (со скидкой)', null=True, blank=True)
    is_present = models.BooleanField('в наличии', default=False)
    views = models.PositiveIntegerField('просмотры', default=0)

    filters = models.ManyToManyField(Filter, related_name='products', verbose_name='фильтры', blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def save(self, *args, **kwargs):
        if not self.slug.strip():
            self.slug = generate_unique_slug_translated(Product, Product.productredirectfrom_set.rel.related_model, self.name)
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
