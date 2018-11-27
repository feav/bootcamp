from django.conf.urls import url
from bootcamp.multimedia import views

urlpatterns = [
	url(r'^$', views.multimedias, name='multimedias'),
	#url(r'^write/$', views.CreateMultimedia.as_view(), name='write'),
    # url(r'^$', views.articles, name='articles'),
    # url(r'^write/$', views.CreateArticle.as_view(), name='write'),
    # url(r'^preview/$', views.preview, name='preview'),
     url(r'^drafts/$', views.drafts, name='drafts'),
       url(r'^bloc_tag/(?P<bloc>.+)/$', views.bloc_tag, name='bloc_tag'),
    # url(r'^comment/$', views.comment, name='comment'),
    
    # url(r'^edit/(?P<pk>\d+)/$',
    #     views.EditArticle.as_view(), name='edit_article'),

    #url(r'^edit/(?P<pk>\d+)/$',
       # views.EditMultimedia.as_view(), name='edit_multimedia'),
    # url(r'^(?P<slug>[-\w]+)/$', views.article, name='article'),

    url(r'^(?P<slug>[-\w]+)/$', views.multimedia, name='multimedia'),
]
