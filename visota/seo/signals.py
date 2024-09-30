from django.db.models.signals import post_save, m2m_changed
from apps.products.signals import full_product_save_admin, full_category_save_admin
from parler.signals import post_translation_save
from django.dispatch import receiver
from apps.products.models import SubCategory, Product, CharValue
from apps.blog.models import Post
from seo.models import SEOCategoryPage, SEOProductPage, SEOPostPage, MetaGenerationRule


@receiver(post_save, sender=SubCategory, dispatch_uid="saveCategory")
def create_category_seo_page(sender, instance, created, **kwargs):
  if created:
    seo_product_page, _ = SEOCategoryPage.objects.get_or_create(product=instance)


@receiver(full_category_save_admin, sender=SubCategory, dispatch_uid="fullCategorySaveAdmin")
def create_category_seo(sender, instance, changed, **kwargs):
  if changed:
    sub_category = instance
    lang = instance.language_code
    seo_category_page, created = SEOCategoryPage.objects.get_or_create(category=sub_category)
    try:
      rule = MetaGenerationRule.objects.get(type='ctg', translations__language_code=lang)
      title = rule.title.format(name=instance.name, description=instance.description)
      description = rule.description.format(name=instance.name, description=instance.description)
    except MetaGenerationRule.DoesNotExist:
      title = instance.name
      description = instance.description

    if seo_category_page.has_translation(language_code=lang):
      translation = seo_category_page.get_translation(lang)
      translation.title = title
      translation.description = description
      seo_category_page.save_translation(translation)
    else:
      seo_category_page.create_translation(lang, title=title, description=description)


@receiver(post_save, sender=Product, dispatch_uid="saveProduct")
def create_product_seo_page(sender, instance, created, **kwargs):
  if created:
    seo_product_page, _ = SEOProductPage.objects.get_or_create(product=instance)


@receiver(full_product_save_admin, sender=Product, dispatch_uid="fullProductSaveAdmin")
def create_product_seo(sender, instance, changed, **kwargs):
  if changed:
    product = instance
    lang = instance.language_code
    seo_product_page, _ = SEOProductPage.objects.get_or_create(product=product)
    try:
      rule = MetaGenerationRule.objects.get(type='prd', translations__language_code=lang)
      
      price = product.current_price or product.actual_price or ''
      cats_q = SubCategory.objects.language(lang).filter(products=instance, translations__language_code=lang)
      cats = ', '.join([c.name for c in cats_q])
      chars_q = CharValue.objects.language(lang).filter(product=instance, translations__language_code=lang)
      chars = '; '.join(['{} - {}'.format(char.key, char.value) for char in chars_q])
      
      title = rule.title.format(name=instance.name, price=price, cats=cats, chars=chars)
      description = rule.description.format(name=instance.name, price=price, cats=cats, chars=chars)
    except MetaGenerationRule.DoesNotExist:
      title = instance.name
      description = instance.name

    if seo_product_page.has_translation(language_code=lang):
      translation = seo_product_page.get_translation(lang)
      translation.title = title
      translation.description = description
      seo_product_page.save_translation(translation)
    else:
      seo_product_page.create_translation(lang, title=title, description=description)


@receiver(post_translation_save, sender=Post, dispatch_uid="createPostTranslation")
def create_post_seo(sender, instance, created, **kwargs):
  if created:
    post = Post.objects.get(pk=instance.master_id)
    seo_post_page, created = SEOPostPage.objects.get_or_create(post=post)
    seo_post_page.create_translation(instance.language_code, title=instance.title, description=instance.content_concise)