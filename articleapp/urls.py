from django.urls import path

from articleapp.views import ArticleCreateView

app_name = 'articleapp'

urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='create'),
]