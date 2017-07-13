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
	url(r'^question/downvote/(?P<pkey>\d+)/$',views.upvote_question,name="downvote_question"),
	url(r'^answer/upvote/(?P<pkey>\d+)/$',views.upvote_answer,name="upvote_answer"),
	url(r'^answer/downvote/(?P<pkey>\d+)/$',views.upvote_answer,name="downvote_answer"),
	url(r'^comment/upvote/(?P<pkey>\d+)/$',views.upvote_comment,name="upvote_comment"),
	url(r'^comment/downvote/(?P<pkey>\d+)/$',views.upvote_comment,name="downvote_comment"),
	url(r'^question/add/$',views.add_question,name="add_question"),
	url(r'^question/edit/(?P<pkey>\d+)/$',views.edit_question,name="edit_question"),
	url(r'^answer/add/(?P<pkey>\d+)/$',views.add_answer,name="add_answer"),
	url(r'^answer/edit/(?P<pkey>\d+)/$',views.edit_answer,name="edit_answer"),
	url(r'^comment/add/(?P<pkey>\d+)/$',views.add_comment,name="add_comment"),
	url(r'^comment/edit/(?P<pkey>\d+)/$',views.edit_comment,name="edit_comment"),
	url(r'^profile/follow/(?P<pkey>\d+)/$',views.follow_profile,name="follow_profile"),
	url(r'^question/follow/(?P<pkey>\d+)/$',views.follow_question,name="follow_question"),
	url(r'^profile/editdetail/$',views.edit_detail,name="edit_detail"),
	url(r'^profile/updatepassword/$',views.update_password,name="update_password"),
]