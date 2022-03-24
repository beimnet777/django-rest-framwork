
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('articles', views.ArticleModelView,basename="articles")


urlpatterns = [
    path('api/v1',views.articles_list),
    path('api/v1/<int:pk>',views.article_item),
    path('api/v1/generics/<str:id>',views.ArticleList.as_view()),
    path('api/v1/model/',include(router.urls)),
     
]