
from django.urls import path
from . import views

urlpatterns = [
    path('api/v1',views.articles_list),
    path('api/v1/<int:pk>',views.article_item),
    path('api/v1/generics/<str:id>',views.ArticleList.as_view()),
     
]