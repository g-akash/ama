from django.conf.urls import url
from . import views

urlpatterns =[
	url(r'^profile/(?P<pkey>\d+)/$',views.profile,name='profile'),
	url(r'^question/(?P<pkey>\d+)/$',views.question,name='question'),
	url(r'^answer/(?P<pkey>\d+)/$',views.answer,name='answer'),
	url(r'^signup/$',views.signup,name='signup'),
	url(r'^login/$',views.login,name='login'),
	url(r'^logout/$',views.logout,name='logout'),
	url(r'^question/upvote/(?P<pkey>\d+)/$',views.upvote_question,name="upvote_question"),
	url(r'^question/downvote/(?P<pkey>\d+)/$',views.downvote_question,name="downvote_question"),
	url(r'^answer/upvote/(?P<pkey>\d+)/$',views.upvote_answer,name="upvote_answer"),
	url(r'^answer/downvote/(?P<pkey>\d+)/$',views.downvote_answer,name="downvote_answer"),
	url(r'^comment/upvote/(?P<pkey>\d+)/$',views.upvote_comment,name="upvote_comment"),
	url(r'^comment/downvote/(?P<pkey>\d+)/$',views.downvote_comment,name="downvote_comment"),


]