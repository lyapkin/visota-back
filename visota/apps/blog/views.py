from rest_framework import viewsets
from rest_framework.response import Response

from .models import *
from .serializers import *


class ArticleApi(viewsets.ReadOnlyModelViewSet):
    lookup_field = "translations__slug"
    queryset = Post.objects.translated().order_by("-id")
    serializer_action_classes = {
        "list": ArticlePreviewSerializer,
        "retrieve": ArticleSerializer
    }

    def get_queryset(self):
        return Post.objects.translated().order_by("-id")

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]
