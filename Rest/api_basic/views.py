


import re
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse ,JsonResponse
from .models import Article
from .serializer import ArticleSerializer,UserSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics,mixins
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


import jwt,datetime


# Create your views here.

class ArticleList(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
  serializer_class=ArticleSerializer
  queryset=Article.objects.all()
  lookup_field='id'
  authentication_calsses=[TokenAuthentication,]
  permission_classes = [IsAuthenticated]
  def get(self,request,id=None):
    if id=="*":
      return self.list(request)
    else:
      return self.retrieve(request)
    
  def post(self,request):
    return self.create(request)
  def put(self,request,id=None):
    return self.update(request)
  def delete(self,request,id=None):
    return self.destroy(request)

class ArticleModelView(viewsets.ModelViewSet):
  queryset=Article.objects.all()
  serializer_class=ArticleSerializer

class UserModelView(viewsets.ModelViewSet):
  queryset=User.objects.all()
  serializer_class=UserSerializer

  
  def create(self,request):
    user=User.objects.create(username=request.POST['username'],
    first_name=request.POST['first_name'],
    last_name=request.POST['last_name'],
    email=request.POST['email'],
    password=request.POST['password'])
    user.save()
class login(APIView):
  def post(self,request):
   
    user=authenticate(request,username=request.data['username'],password=request.data['password'])
    
    if user:
      payload={
      'id':user.id,
      'exp':datetime.datetime.utcnow() +datetime.timedelta(hours=1.0),
      'iat':datetime.datetime.utcnow()}
      token=jwt.encode(payload,'secret',algorithm='HS256')
      response=Response()
      response.data={
        'jwt':token
      }
      return response
    return Response(status=status.HTTP_401_UNAUTHORIZED)









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

  

