from django.urls import path

from .views import ForumView, ReplyCorrectView, ThreadView

app_name = 'forum'

urlpatterns = [
    path('', ForumView.as_view(), name='index'),
    path('<slug>/', ThreadView.as_view(), name='thread'),
    path('respostas/<pk>/correta/', ReplyCorrectView.as_view(), name='reply_correct'),
    path(
        'respostas/<pk>/incorreta/', ReplyCorrectView.as_view(correct=False),
        name='reply_incorrect'
    ),
    path('tag/<tag>/', ForumView.as_view(), name='index_tagged'),
]
