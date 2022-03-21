import imp
from telnetlib import STATUS
from django.shortcuts import render
from django.http import HttpResponse ,JsonResponse
from .models import Article
from .serializer import ArticleSerializer
from rest_framework.parsers import JSONParser


# Create your views here.
def articles_list(request):
  if request.method=='POST':
    pass
  articles=Article.objects.all()
  serializer=ArticleSerializer(articles,many=True)
  return JsonResponse(serializer.data,status=200,safe=False)