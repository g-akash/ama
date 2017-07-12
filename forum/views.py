# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.models import User
from django.contrib.auth import logout as Logout
from django.contrib.auth import login as Login
from .models import Question, Answer, Profile
from .forms import SignupForm, LoginForm

from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='/login/')
def profile(request,pkey):
	user = get_object_or_404(User, pk=pkey)
	profilee = get_object_or_404(Profile,user=user)
	questions = Question.objects.filter(author=user).order_by('created_date')
	return render(request,'forum/profile.html',{'questions':questions,'profile':profilee})

@login_required(login_url='/login/')
def question(request,pkey):
	question = get_object_or_404(Question,pk=pkey)
	answers = Answer.objects.filter(question=question).order_by('-created_date')
	return render(request,'forum/question.html',{'question':question,'answers':answers})

@login_required(login_url='/login/')
def answer(request,pkey):
	answer = get_object_or_404(Answer,pk=pkey)
	question = answer.question
	return render(request,'forum/answer.html',{'question':question,'answer':answer})

@login_required
def upvote_question(request,pkey):
	user = request.user
	question = get_object_or_404(Question,pk=pkey)
	q_upvote = Q_upvote.objects.filter(upvoter=user,question=question)
	if q_upvote is None:
		q_upvote = Q_upvote(upvoter=user,question=question)
		q_upvote.save()
	return redirect(requst.META['HTTP_REFERER'])

@login_required
def downvote_question(request,pkey):
	user = request.user
	question = get_object_or_404(Question,pk=pkey)
	q_upvote = Q_upvote.objects.filter(upvoter=user,question=question)
	if q_upvote is not None:
		q_upvote.delete()
	return redirect(requst.META['HTTP_REFERER'])


@login_required
def upvote_answer(request,pkey):
	user = request.user
	answer = get_object_or_404(Answer,pk=pkey)
	a_upvote = A_upvote.objects.filter(upvoter=user,answer=answer)
	if a_upvote is None:
		a_upvote = A_upvote(upvoter=user,answer=answer)
		a_upvote.save()
	return redirect(requst.META['HTTP_REFERER'])

@login_required
def downvote_answer(request,pkey):
	user = request.user
	answer = get_object_or_404(Answer,pk=pkey)
	a_upvote = A_upvote.objects.filter(upvoter=user,answer=answer)
	if a_upvote is not None:
		a_upvote.delete()
	return redirect(requst.META['HTTP_REFERER'])



@login_required
def upvote_comment(request,pkey):
	user = request.user
	comment = get_object_or_404(Comment,pk=pkey)
	c_upvote = C_upvote.objects.filter(upvoter=user,comment=comment)
	if c_upvote is None:
		c_upvote = C_upvote(upvoter=user,comment=comment)
		c_upvote.save()
	return redirect(requst.META['HTTP_REFERER'])

@login_required
def downvote_comment(request,pkey):
	user = request.user
	comment = get_object_or_404(Comment,pk=pkey)
	c_upvote = C_upvote.objects.filter(upvoter=user,comment=comment)
	if c_upvote is not None:
		c_upvote.delete()
	return redirect(requst.META['HTTP_REFERER'])



# @login_required
# def add_question(request):
# 	if request.method=="POST":
		



# @login_required
# def edit_question(request,pkey):


# @login_required
# def add_answer(request,pkey):


# @login_required
# def edit_answer(request,pkey):


# @login_required
# def add_comment(request,pkey):


# @login_required
# def edit_comment(request,pkey):





def signup(request):
	if request.method == "POST":
		print request.POST
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			profile = Profile()
			profile.user = user
			profile.save()
			print "printing user info."
			print user
			print user.pk
			return redirect('profile',pkey=user.pk)
	else:
		form = SignupForm()
	return render(request,"forum/signup.html",{'form':form})

def login(request):
	if request.method == "POST":
		form = LoginForm(request,request.POST)
		if form.is_valid():
			data = form.cleaned_data
			user = get_object_or_404(User,username=data['username'])
			if user.check_password(data['password']):
				Login(request,user)
				return redirect('profile',pkey=user.pk)

	else:
		form = LoginForm()
	return render(request,"forum/login.html",{'form':form})


def logout(request):
	Logout(request)
	form = LoginForm()
	return render(request,"forum/login.html",{'form':form})
