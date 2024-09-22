from django.db.models.signals import post_save
from parler.signals import post_translation_save
from django.dispatch import receiver
from apps.products.models import SubCategory, Product
from apps.blog.models import Post
from seo.models import SEOCategoryPage, SEOProductPage, SEOPostPage


@receiver(post_translation_save, sender=SubCategory, dispatch_uid="createCatTranslation")
def create_category_seo(sender, instance, created, **kwargs):
  if created:
    sub_category = SubCategory.objects.get(pk=instance.master_id)
    seo_category_page, created = SEOCategoryPage.objects.get_or_create(category=sub_category)
    seo_category_page.create_translation(instance.language_code, title=instance.name, description=instance.name)


@receiver(post_translation_save, sender=Product, dispatch_uid="createProductTranslation")
def create_product_seo(sender, instance, created, **kwargs):
  if created:
    product = Product.objects.get(pk=instance.master_id)
    seo_product_page, created = SEOProductPage.objects.get_or_create(product=product)
    seo_product_page.create_translation(instance.language_code, title=instance.name, description=instance.name)


@receiver(post_translation_save, sender=Post, dispatch_uid="createPostTranslation")
def create_post_seo(sender, instance, created, **kwargs):
  if created:
    post = Post.objects.get(pk=instance.master_id)
    seo_post_page, created = SEOPostPage.objects.get_or_create(post=post)
    seo_post_page.create_translation(instance.language_code, title=instance.title, description=instance.content_concise)