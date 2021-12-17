from django.urls import path

from articleapp.views import ArticleCreateView, ArticleDetailView

app_name = 'articleapp'

urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('detail/<int:pk>', ArticleDetailView.as_view(), name='detail'),
]
