from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^(?P<pkey>\d+)/$',views.question,name='question'),
]