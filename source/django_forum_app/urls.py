from django.conf.urls import url
from django_forum_app import views
from django.urls import path
app_name = 'django_forum_app'

urlpatterns = [
    # url(r'^$', views.index, name='forum-index'),
    # url(r'^(?P<slug>[-\w]+)/$', views.forum, name='forum-detail'),
    # url(r'^(?P<slug>[-\w]+)/(?P<topic_id>\d+)/$', views.topic, name='topic-detail'),
    # url(r'^(?P<slug>[-\w]+)/(?P<topic_id>\d+)/close$', views.close_topic, name='close-topic'),
    # url(r'^(?P<slug>[-\w]+)/(?P<topic_id>\d+)/reply/$', views.post_reply, name='reply'),
    # url(r'(?P<slug>[-\w]+)/newtopic/$', views.new_topic, name='new-topic'),

    path('', views.index, name='forum-index'),
    path('feed', views.feed, name='feed'),
    path('fresh', views.fresh_feed, name='fresh'),
    path('vote-object', views.vote_object, name='vote-object'),
    path('notifications', views.view_notificatoins, name='view-notifications'),
    path('search-topic', views.search_topic, name='search-topic'),
    path('<str:slug>', views.forum, name='forum-detail'),
    path('<int:post_id>/add-comment', views.add_comment_to_post, name='add-comment'),
    path('<int:comment_id>/edit-comment', views.edit_comment, name='edit-comment'),
    path('<int:comment_id>/delete-comment', views.delete_comment, name='delete-comment'),
    path('<str:slug>/newtopic', views.new_topic, name='new-topic'),
    path('<str:slug>/<int:topic_id>', views.topic, name='topic-detail'),
    path('<str:slug>/<int:topic_id>/close', views.close_topic, name='close-topic'),
    path('<str:slug>/<int:topic_id>/reply', views.post_reply, name='reply'),
    path('<str:forum_slug>/<int:topic_id>/<int:pk>', views.post_detail, name='post-detail'),
    path('<str:forum_slug>/<int:topic_id>/delete-post/<int:pk>', views.delete_post, name='delete-post'),

    
]
