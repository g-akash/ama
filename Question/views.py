# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Question, Q_follow
from Answer.models import Answer
from Profile.models import Profile, P_follow

# Create your views here.

def question(request,pkey):
	question = get_object_or_404(Question,pk=pkey)
	answers = Answer.objects.filter(question=question).order_by('created_date')
	num_followers = Q_follow.objects.filter(question=question).count()
	return render(request,'Question/question.html',{'question':question,'answers':answers})


