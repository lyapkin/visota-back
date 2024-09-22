from django.db import models
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
  

class SEOStaticPage(TranslatableModel):
  order = models.PositiveSmallIntegerField('позиция (сортировка списка в админке)')
  page = models.CharField(max_length=64, primary_key=True)
  name = models.CharField('страница', max_length=255, unique=True)
  translations = TranslatedFields(
    header = models.CharField("h1", max_length=255, unique=True),
    title = models.CharField("title", max_length=255),
    description = models.TextField('description'),
    noindex_follow = models.BooleanField('<meta name="robots" content="noindex, follow">', default=False)
  )

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
    noindex_follow = models.BooleanField('<meta name="robots" content="noindex, follow">', default=False)
  )

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
    noindex_follow = models.BooleanField('<meta name="robots" content="noindex, follow">', default=False)
  )

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
    noindex_follow = models.BooleanField('<meta name="robots" content="noindex, follow">', default=False)
  )

  def __str__(self):
    return self.post.title
    
  class Meta:
    verbose_name = "SEO для поста"
    verbose_name_plural = "SEO для поста"