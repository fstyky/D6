from django.urls import path
# Импортируем созданное нами представление
from .views import PostDelete,ArticleCreate,PostsList, PostDetail,\
   PostsSearch,NewsCreate,NewUpdate,ArticleUpdate, CategoryList, subscribe


urlpatterns = [

   path('', PostsList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search/', PostsSearch.as_view(), name='post_search'),
   path('news/create/', NewsCreate.as_view()),
   path('articles/create/', ArticleCreate.as_view()),
   path('articles/<int:pk>/edit/', NewUpdate.as_view()),
   path('news/<int:pk>/edit/', ArticleUpdate.as_view()),
   path('articles/<int:pk>/delete/', PostDelete.as_view()),
   path('news/<int:pk>/delete/', PostDelete.as_view()),
   path('categories/<int:pk>',CategoryList.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe',subscribe,name='subscribe')
]