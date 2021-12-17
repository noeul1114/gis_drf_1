from django.urls import path

from articleapp.views import ArticleCreateView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView, \
    MagicGridTemplateView

app_name = 'articleapp'

urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('detail/<int:pk>', ArticleDetailView.as_view(), name='detail'),
    path('update/<int:pk>', ArticleUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', ArticleDeleteView.as_view(), name='delete'),

    path('magic_grid/', MagicGridTemplateView.as_view(), name='magic_grid'),
]
