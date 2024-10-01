import os
from decimal import Decimal
from typing import Iterable
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from parler.models import TranslatableModel, TranslatedFields
from apps.products.models import SubCategory, Product
from apps.blog.models import Post

# Create your models here.
class Robots(models.Model):
  text = models.TextField('robots.txt')

  class Meta:
    verbose_name = 'Robots'
    verbose_name_plural = 'Robots'

  def __str__(self) -> str:
    return 'robots.txt'
  

CHANGE_FREQ_CHOICES = {
  'always': 'always',
  'hourly': 'hourly',
  'daily': 'daily',
  'weekly': 'weekly',
  'monthly': 'monthly',
  'yearly': 'yearly',
  'never': 'never'
}
  

class Sitemap(models.Model):
  pass

  

class SEOStaticPage(TranslatableModel):
  order = models.PositiveSmallIntegerField('позиция (сортировка списка в админке)')
  page = models.CharField(max_length=64, primary_key=True)
  name = models.CharField('страница', max_length=255, unique=True)
  translations = TranslatedFields(
    header = models.CharField("h1", max_length=255, unique=True),
    title = models.CharField("title", max_length=255),
    description = models.TextField('description'),
    noindex_follow = models.BooleanField('<meta name="robots" content="noindex, follow">', default=False),
    change_freq = models.CharField('changefreq', max_length=7, choices=CHANGE_FREQ_CHOICES, default='yearly'),
    priority = models.DecimalField('priority', max_digits=2, decimal_places=1, validators=[MinValueValidator(Decimal('0.1')), MaxValueValidator(Decimal('1.0'))], default=1.0)
  )

  sitemap = models.ForeignKey(Sitemap, related_name='statics', on_delete=models.PROTECT, default=1)

  def __str__(self):
    return self.name
    
  class Meta:
    verbose_name = "SEO для статических страниц"
    verbose_name_plural = "SEO для статических страниц"
    ordering = ('order',)


class SEOCategoryPage(TranslatableModel):
  category = models.OneToOneField(SubCategory, verbose_name='категория', related_name='seo', on_delete=models.CASCADE, primary_key=True)
  translations = TranslatedFields(
    title = models.CharField("title", max_length=255),
    description = models.TextField('description'),
    noindex_follow = models.BooleanField('<meta name="robots" content="noindex, follow">', default=False),
    change_freq = models.CharField('changefreq', max_length=7, choices=CHANGE_FREQ_CHOICES, default='yearly'),
    priority = models.DecimalField('priority', max_digits=2, decimal_places=1, validators=[MinValueValidator(Decimal('0.1')), MaxValueValidator(Decimal('1.0'))], default=1.0)
  )

  sitemap = models.ForeignKey(Sitemap, related_name='categories', on_delete=models.PROTECT, default=1)

  def __str__(self):
    return self.category.name
    
  class Meta:
    verbose_name = "SEO для категорий"
    verbose_name_plural = "SEO для категорий"


class SEOProductPage(TranslatableModel):
  product = models.OneToOneField(Product, verbose_name='Товар', related_name='seo', on_delete=models.CASCADE, primary_key=True)
  translations = TranslatedFields(
    title = models.CharField("title", max_length=255),
    description = models.TextField('description'),
    noindex_follow = models.BooleanField('<meta name="robots" content="noindex, follow">', default=False),
    change_freq = models.CharField('changefreq', max_length=7, choices=CHANGE_FREQ_CHOICES, default='yearly'),
    priority = models.DecimalField('priority', max_digits=2, decimal_places=1, validators=[MinValueValidator(Decimal('0.1')), MaxValueValidator(Decimal('1.0'))], default=1.0)
  )

  sitemap = models.ForeignKey(Sitemap, related_name='products', on_delete=models.PROTECT, default=1)

  def __str__(self):
    return self.product.name
    
  class Meta:
    verbose_name = "SEO для товара"
    verbose_name_plural = "SEO для товара"


class SEOPostPage(TranslatableModel):
  post = models.OneToOneField(Post, verbose_name='пост', related_name='seo', on_delete=models.CASCADE, primary_key=True)
  translations = TranslatedFields(
    title = models.CharField("title", max_length=255),
    description = models.TextField('description'),
    noindex_follow = models.BooleanField('<meta name="robots" content="noindex, follow">', default=False),
    change_freq = models.CharField('changefreq', max_length=7, choices=CHANGE_FREQ_CHOICES, default='yearly'),
    priority = models.DecimalField('priority', max_digits=2, decimal_places=1, validators=[MinValueValidator(Decimal('0.1')), MaxValueValidator(Decimal('1.0'))], default=1.0)
  )

  sitemap = models.ForeignKey(Sitemap, related_name='posts', on_delete=models.PROTECT, default=1)

  def __str__(self):
    return self.post.title
    
  class Meta:
    verbose_name = "SEO для поста"
    verbose_name_plural = "SEO для поста"


class MetaGenerationRule(TranslatableModel):
  choices = {
    'ctg': 'Категория',
    'prd': 'Товар'
  }

  type = models.CharField('тип', max_length=3, choices=choices)
  instruction = models.TextField('инструкция')
  translations = TranslatedFields(
    title = models.CharField('правило генерации Title', max_length=255),
    description = models.CharField('правило генерации Description', max_length=255)
  )

  def __str__(self):
    return self.choices[self.type]
    
  class Meta:
    verbose_name = "правило генерации метатегов"
    verbose_name_plural = "правила генерации метатегов"


class AbstractFile(models.Model):
  name = models.CharField('название', max_length=30, unique=True)
  content = models.TextField('код', null=True, blank=True)

  def __str__(self):
    return self.name

  class Meta:
    abstract = True


class JSFile(AbstractFile):
    
  class Meta:
    verbose_name = "js"
    verbose_name_plural = "js"

  def save(self, *args, **kwargs):
    os.makedirs(os.path.join(settings.STATIC_ROOT, 'seo', 'js'), exist_ok=True)
    with open(os.path.join(settings.STATIC_ROOT, 'seo', 'js', self.name), 'w') as f:
      file = File(f)
      file.write(self.content)
    super().save(*args, **kwargs)


class CSSFile(AbstractFile):
    
  class Meta:
    verbose_name = "css"
    verbose_name_plural = "css"

  def save(self, *args, **kwargs):
    os.makedirs(os.path.join(settings.STATIC_ROOT, 'seo', 'css'), exist_ok=True)
    with open(os.path.join(settings.STATIC_ROOT, 'seo', 'css', self.name), 'w') as f:
      file = File(f)
      file.write(self.content)
    super().save(*args, **kwargs)