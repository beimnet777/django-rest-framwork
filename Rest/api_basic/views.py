
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


@csrf_exempt
def article_item(request,pk):
  try:
    article=Article.objects.get(id=pk)
  except Article.DoesNotExist:
    return HttpResponse(status=404)
  
  if request.method=='PUT':
    data=JSONParser().parse(request)

    serializer=ArticleSerializer(article,data)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(serializer.data,status=202)
    else:
      return JsonResponse(serializer.errors,status=400)

  elif request.method=='DELETE':
    article.delete()
    return HttpResponse(status=204)
  else:
    serializer=ArticleSerializer(article)
    return JsonResponse(serializer.data,status=200,safe=False)

