
from django.shortcuts import render
from django.http import HttpResponse ,JsonResponse
from .models import Article
from .serializer import ArticleSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
@api_view(['GET','POST'])
def articles_list(request):
  if request.method=='POST':
   
    serialized=ArticleSerializer(data=request.data)
    if serialized.is_valid():
      serialized.save()
      return Response(serialized.data,status=status.HTTP_201_CREATED)
    else:
      return Response(serialized.errors,status=status.HTTP_400_BAD_REQUEST)
  articles=Article.objects.all()
  serializer=ArticleSerializer(articles,many=True)
  return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET','PUT','DELETE'])
def article_item(request,pk):
  try:
    article=Article.objects.get(id=pk)
  except Article.DoesNotExist:
    return HttpResponse(status=status.HTTP_404_NOT_FOUND)
  
  if request.method=='PUT':
    
    serializer=ArticleSerializer(article,request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    else:
      return JsonResponse(serializer.errors,status=status.HTTP_404_NOT_FOUND)

  elif request.method=='DELETE':
    article.delete()
    return HttpResponse(status=status.HTTP_204_NO_CONTENT)
  else:
    serializer=ArticleSerializer(article)
    return Response(serializer.data,status=status.HTTP_200_OK)

