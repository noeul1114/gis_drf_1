from django.http import HttpResponseForbidden

from articleapp.models import Article


def article_ownership_required(func):
    def decorated(request, *args, **kwargs):
        target_article = Article.objects.get(pk=kwargs['pk'])
        if not target_article.writer == request.user:
            return HttpResponseForbidden()
        else:
            return func(request, *args, **kwargs)
    return decorated
