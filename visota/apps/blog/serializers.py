from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers
from django.conf import settings

from .models import *


class ContentFieldSerializer(serializers.Field):
    def to_representation(self, value):
        domain = 'http://'+str(get_current_site(self.context['request']))
        if self.context['request'].is_secure():
            domain = 'https://'+str(get_current_site(self.context['request']))
        content = value.replace("src=\"/media/", f"src=\"{domain}/media/")
        content = content.replace("&lt;", "<")
        content = content.replace("&gt;", ">")
        content = content.replace("&quot;", "")
        return content
    

class ArticleSerializer(serializers.ModelSerializer):
    content = ContentFieldSerializer()

    class Meta:
        model = Post
        fields = ("id", "title", "content", "date")


class ArticlePreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            "title",
            'slug',
            'content_concise',
            'date',
            'image_url',
            )