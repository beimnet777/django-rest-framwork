from http import server
import imp
from telnetlib import STATUS
from django.shortcuts import render
from django.http import HttpResponse ,JsonResponse
from .models import Article
from .serializer import ArticleSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def articles_list(request):
  if request.method=='POST':
    data =JSONParser().parse(request)
    serialized=ArticleSerializer(data=data)
    if serialized.is_valid():
      serialized.save()
      return JsonResponse(serialized.data,status=201)
    else:
      return JsonResponse(serialized.errors,status=400)
  articles=Article.objects.all()
  serializer=ArticleSerializer(articles,many=True)
  return JsonResponse(serializer.data,status=200,safe=False)