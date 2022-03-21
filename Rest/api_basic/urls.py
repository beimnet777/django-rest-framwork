
from django.urls import path
from . import views

urlpatterns = [
    path('',views.articles_list),
    path('<int:pk>',views.article_item),
     
]