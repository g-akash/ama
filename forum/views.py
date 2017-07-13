# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.models import User
from django.contrib.auth import logout as Logout
from django.contrib.auth import login as Login
from .models import Question, Answer, Profile
from .models import Q_upvote, A_upvote, C_upvote
from .models import Q_follow, P_follow
from .forms import SignupForm, LoginForm
from .forms import QuestionForm, AnswerForm, CommentForm
from .forms import EditDetailForm, ChangePasswordForm

from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='/login/')
def profile(request,pkey):
	profile = get_object_or_404(Profile, pk=pkey)
	user = profile.user
	questions = Question.objects.filter(author=user).order_by('created_date')
	return render(request,'forum/profile.html',{'questions':questions,'profile':profile})

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


####################
# updating details

@login_required(login_url='/login/')
def edit_detail(request):
	if request.method=="POST":
		form = EditDetailForm(request.POST)
		if form.is_valid():
			user = request.user
			user.email = form.cleaned_data['email']
			user.save()
			return redirect('profile',pkey=user.pk)
	else:
		form = EditDetailForm()
	return render(request,'forum/edit_detail.html',{'form':form})



@login_required(login_url='/login/')
def update_password(request):
	if request.method=="POST":
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			user = request.user
			data = form.cleaned_data
			
			user.set_password(data['password1'])
			return redirect(profile, pkey=user.pk)
	else:
		form = ChangePasswordForm()
	return render(request,'forum/update_password.html',{'form':form})




#####################
# upvoting and downvoting question, answer and comment

@login_required(login_url='/login/')
def upvote_question(request,pkey):
	user = request.user
	question = get_object_or_404(Question,pk=pkey)
	q_upvote = Q_upvote.objects.filter(upvoter=user,question=question)
	if not q_upvote:
		q_upvote = Q_upvote(upvoter=user,question=question)
		q_upvote.save()
	else:
		q_upvote.delete()
	return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='/login/')
def upvote_answer(request,pkey):
	user = request.user
	answer = get_object_or_404(Answer,pk=pkey)
	a_upvote = A_upvote.objects.filter(upvoter=user,answer=answer)
	if not a_upvote:
		a_upvote = A_upvote(upvoter=user,answer=answer)
		a_upvote.save()
	else:
		a_upvote.delete()
	return redirect(request.META['HTTP_REFERER'])




@login_required(login_url='/login/')
def upvote_comment(request,pkey):
	user = request.user
	comment = get_object_or_404(Comment,pk=pkey)
	c_upvote = C_upvote.objects.filter(upvoter=user,comment=comment)
	if not c_upvote:
		c_upvote = C_upvote(upvoter=user,comment=comment)
		c_upvote.save()
	else:
		c_upvote.delete()
	return redirect(request.META['HTTP_REFERER'])




######################
# following a question or user or topic

@login_required(login_url='/login/')
def follow_question(request,pkey):
	user = request.user
	question = get_object_or_404(Question,pk=pkey)
	q_follow = Q_follow.objects.filter(question=question,follower=user)
	if not q_follow:
		q_follow = Q_follow(question=question,follower=user)
		q_follow.save()
	else:
		q_follow.delete()
	return redirect(request.META['HTTP_REFERER'])




@login_required(login_url='/login/')
def follow_profile(request,pkey):
	follower = get_object_or_404(Profile,user=request.user)
	followee = get_object_or_404(Profile,pk=pkey)
	p_follow = P_follow.objects.filter(follower=follower,followee=followee)
	print "printing p_follow"
	print p_follow
	if not p_follow:
		p_follow = P_follow()
		p_follow.follower = follower
		p_follow.followee = followee
		p_follow.save()
		print "new follow"
		print p_follow.pk
		print p_follow
	else:
		print "deleted the follow"
		p_follow.delete()

	return redirect(request.META['HTTP_REFERER'])


	



@login_required(login_url='/login/')
def add_question(request):
	if request.method=="POST":
		form = QuestionForm(request.POST)
		if form.is_valid():
			question = Question()
			question.text = form.cleaned_data['text']
			question.author = request.user
			question.save()
			return redirect('question',pkey=question.pk)
	else:
		form = QuestionForm()
	return render(request,'forum/add_question.html',{'form':form})



@login_required(login_url='/login/')
def edit_question(request,pkey):
	question = get_object_or_404(Question,pk=pkey)
	if request.method=="POST":
		form = QuestionForm(request.POST)
		if form.is_valid():
			if question.author == request.user:
				question.text = form.cleaned_data['text']
				question.save()
				return redirect('question',pkey=question.pk)
	else:
		form = QuestionForm(instance=question)
	return render(request,'forum/add_question.html',{'form':form})


@login_required(login_url='/login/')
def add_answer(request,pkey):
	if request.method=="POST":
		form = AnswerForm(request.POST)
		if form.is_valid():
			answer = Answer()
			answer.text = form.cleaned_data['text']
			answer.author = request.user
			question = get_object_or_404(Question,pk=pkey)
			answer.question = question
			answer.save()
			return redirect('answer',pkey=answer.pk)

	else:
		form = AnswerForm()

	return render(request,'forum/add_answer.html',{'form':form})



@login_required(login_url='/login/')
def edit_answer(request,pkey):
	answer = get_object_or_404(Answer,pk=pkey)
	if request.method == "POST":
		form = AnswerForm(request.POST)
		if form.is_valid():
			if answer.author == request.user:
				answer.text = form.cleaned_data['text']
				answer.save()
				return redirect('answer',pkey=answer.pk)
	else:
		form = AnswerForm(instance=answer)
	return render(request,'forum/add_answer.html',{'form':form})



@login_required(login_url='/login/')
def add_comment(request,pkey):
	if request.method=="POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = Comment()
			comment.text = form.cleaned_data['text']
			answer = get_object_or_404(Answer,pk=pkey)
			comment.author = request.user
			comment.answer = answer
			comment.save()
			return redirect('answer',pkey=answer.pk)
	else:
		form = CommentForm()

	return render(request,'forum/add_comment.html',{'form':form})

@login_required(login_url='/login/')
def edit_comment(request,pkey):
	comment = get_object_or_404(Comment,pk=pkey)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			if comment.author == user:
				comment.text = form.cleaned_data['text']
				comment.save()
				return redirect('answer',pkey=comment.answer.pk)
	else:
		form = CommentForm(instance=comment)
	return render(request,'forum/add_comment.html',{'form':form})



def signup(request):
	if request.method == "POST":
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			profile = Profile()
			profile.user = user
			profile.save()
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
