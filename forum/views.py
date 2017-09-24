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
from .models import Q_follow, P_follow, Ppic, Related_topic
from .models import Topic
from .forms import SignupForm, LoginForm
from .forms import QuestionForm, AnswerForm, CommentForm
from .forms import EditDetailForm, ChangePasswordForm
from .forms import PpicForm
from django.contrib.auth.decorators import login_required

from django.conf import settings

import random
from operator import itemgetter 

# Create your views here.


def get_answers_from_followees(user):
	profile = get_object_or_404(Profile,user=user)
	followees = profile.get_followees_user()
	answers = Answer.objects.filter(author__in=followees)
	return answers

def get_answers_from_topics(user):
	profile = get_object_or_404(Profile,user=user)
	topics = profile.get_topics()
	related_topics = Related_topic.objects.filter(topic__in=topics)
	answers = []
	for related_topic in related_topics:
		answer = related_topic.question.get_one_answer()
		if answer is not None:
			answers.append(answer)

	return answers


def get_answers_from_questions(user):
	profile = get_object_or_404(Profile,user=user)
	questions = []
	questions+=profile.get_questions()
	questions+=profile.get_followed_questions()
	answers = []
	for question in questions:
		answer = question.get_one_answer()
		if answer is not None:
			answers.append(answer)

	return answers


def get_exploratory_answers(user):
	profile = get_object_or_404(Profile,user=user)
	followees = profile.get_followees_user()
	a_upvotes = A_upvote.objects.filter(upvoter__in=followees)
	answers = []
	for upvote in a_upvotes:
		answers.append(upvote.answer)

	return answers


def get_random_answers(num):
	last = Answer.objects.last().pk
	answers=[]
	ans_num=[]
	for i in range(num):
		ans_num.append(random.randint(0,last-1))
	ans_num.sort()
	print ans_num
	answers = itemgetter(*ans_num)(Answer.objects.all())
	return list(answers)


@login_required(login_url='/login')
def home(request):
	# make your list of answers here
	answers_det=[]
	answers_exp=[]
	answers_ran=[]
	answers_det+=get_answers_from_followees(request.user)
	answers_det+=get_answers_from_topics(request.user)
	answers_det+=get_answers_from_questions(request.user)
	answers_exp = get_exploratory_answers(request.user)
	answers_ran = get_random_answers(10)
	# at this point your answer list is complete
	print answers_exp
	answers = answers_det+answers_exp+answers_ran
	answers = list(set(list(answers)))
	answers = sorted(answers,key=lambda x: x.created_date)
	questions=[]
	for i in range(len(answers)):
		questions.append(answers[i].question)

	return render(request,'forum/home.html',{'questions':questions,'answers':answers,'size':len(questions)})




@login_required(login_url='/login/')
def profile(request):
	pkey = request.user.pk
	profile = get_object_or_404(Profile, pk=pkey)
	user = profile.user
	answers = Answer.objects.filter(author=user).order_by('created_date')
	image = "/Users/akash/AMA/ama/pictures/"+str(user)+".jpg"
	return render(request,'forum/profile.html',{'answers':answers,'profile':profile,'img':image})



@login_required(login_url='/login/')
def topic(request,pkey):
	topic = get_object_or_404(Topic,pk=pkey)
	questions = topic.get_questions()
	answers = []
	# for question in questions:
	# 	answers.append(question.get_one_answer())

	return render(request,'forum/topic.html',{'topic':topic,'questions':questions,'answers':answers})



@login_required(login_url='/login/')
def other_profile(request,pkey):
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
			return redirect('profile')
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
			user.save()
			return redirect('profile')
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
		question.change_num_upvotes(1)
		q_upvote.save()
	else:
		question.change_num_upvotes(-1)
		q_upvote.delete()
	return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='/login/')
def upvote_answer(request,pkey):
	user = request.user
	answer = get_object_or_404(Answer,pk=pkey)
	a_upvote = A_upvote.objects.filter(upvoter=user,answer=answer)
	if not a_upvote:
		a_upvote = A_upvote(upvoter=user,answer=answer)
		answer.change_num_upvotes(1)
		a_upvote.save()
	else:
		answer.change_num_upvotes(-1)
		a_upvote.delete()
	return redirect(request.META['HTTP_REFERER'])




@login_required(login_url='/login/')
def upvote_comment(request,pkey):
	user = request.user
	comment = get_object_or_404(Comment,pk=pkey)
	c_upvote = C_upvote.objects.filter(upvoter=user,comment=comment)
	if not c_upvote:
		c_upvote = C_upvote(upvoter=user,comment=comment)
		comment.change_num_upvotes(1)
		c_upvote.save()
	else:
		c_upvote.delete()
		comment.change_num_upvotes(-1)
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
		question.change_num_followers(1)
		q_follow.save()
	else:
		question.change_num_followers(-1)
		q_follow.delete()
	return redirect(request.META['HTTP_REFERER'])




@login_required(login_url='/login/')
def follow_topic(request,pkey):
	user = request.user
	topic = get_object_or_404(Topic,pk=pkey)
	t_follow = T_follow.objects.filter(topic=topic,follower=user)
	if not t_follow:
		t_follow = T_follow(topic=topic,follower=user)
		t_follow.save()
		topic.change_num_followers(1)
	else:
		t_follow.delete()
		topic.change_num_followers(-1)
	return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='/login/')
def follow_profile(request,pkey):
	follower = get_object_or_404(Profile,user=request.user)
	followee = get_object_or_404(Profile,pk=pkey)
	p_follow = P_follow.objects.filter(follower=follower,followee=followee)
	if not p_follow:
		p_follow = P_follow()
		p_follow.follower = follower
		p_follow.followee = followee
		p_follow.save()
		follower.change_num_followees(1)
		followee.change_num_followers(1)
	else:
		p_follow.delete()
		follower.change_num_followees(-1)
		followee.change_num_followers(-1)

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




########################
# upload profile picture

def update_ppic(request):
	if request.method=="POST":
		form = PpicForm(request.POST,request.FILES)
		print request.FILES
		if form.is_valid():
			pic_name = str(request.user) + ".jpg"
			pic = Ppic()
			pic.ppic = request.FILES['ppic']
			with open("/Users/akash/AMA/ama/pictures/"+pic_name, 'wb') as pic:
				for chunk in request.FILES['ppic'].chunks():
					pic.write(chunk)
			return redirect('profile')
	else:
		form = PpicForm()

	return render(request,'forum/update_ppic.html',{'form':form})




def signup(request):
	if request.method == "POST":
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			profile = Profile()
			profile.user = user
			profile.save()
			return redirect('profile')
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
				return redirect('profile')

	else:
		form = LoginForm()
	return render(request,"forum/login.html",{'form':form})


def logout(request):
	Logout(request)
	form = LoginForm()
	return redirect('login')
	# return render(request,"forum/login.html",{'form':form})
