from django.shortcuts import render, HttpResponse
from .models import Robots

# Create your views here.
def robots(req):
  robots = Robots.objects.all()[0]
  return HttpResponse(robots.text, content_type='text/plain')