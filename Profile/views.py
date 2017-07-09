# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect
from Question.models import Question
from django.contrib.auth.models import User


# Create your views here.


def profile(request,pkey):
	user = get_object_or_404(User,pk=pkey)
	questions = Question.objects.filter(author=user).order_by('created_date')
	print questions
	return render(request,'Profile/profile.html',{'questions':questions,'user':user})
