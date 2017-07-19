# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.



###################################
# Model for Profile


class Profile(models.Model):
	user = models.ForeignKey('auth.User')
	num_followers = models.IntegerField(default=0)
	num_followees = models.IntegerField(default=0)

	def change_num_followers(self,k=1):
		self.num_followers+=k
		self.save()

	def change_num_followees(self,k=1):
		self.num_followees+=k
		self.save()

	def get_num_followers(self):
		return self.num_followers

	def get_followers(self):
		followers = P_follow.objects.filter(followee=self)
		return followers

	def get_num_followees(self):
		return self.num_followees

	def get_followees(self):
		p_follows = P_follow.objects.filter(follower=self)
		followees = []
		for p_follow in p_follows:
			followees.append(p_follow.followee)
		return followees

	def get_followees_user(self):
		p_follows = P_follow.objects.filter(follower=self)
		followees = []
		for p_follow in p_follows:
			followees.append(p_follow.followee.user)
		return followees

	def get_num_questions(self):
		num_questions = Question.objects.filter(author=self.user).count()
		return num_questions

	def get_questions(self):
		questions = Question.objects.filter(author=self.user)
		return questions

	def get_followed_questions(self):
		q_follow = Q_follow.objects.filter(follower = self.user)
		questions = []
		for q in q_follow:
			questions.append(q.question)
		return questions

	def get_answers(self):
		answers = Answer.objects.filter(author=self.user)
		return answers


	def get_topics(self):
		topics_follow = T_follow.objects.filter(follower=self.user)
		topics = []
		for topic_follow in topics_follow:
			topics.append(topic_follow.topic)
		return topics


	def getQandA(self):
		questions = Question.objects.filter(author=self.user)
		answers = []
		for question in questions:
			answer = Answer.objects.filter(author=self.user,question=question)
			answers.append(answer)

		return questions, answers


	def __str__(self):
		return str(self.user)

	class Meta:
		unique_together = (("user"),)




class P_follow(models.Model):
	follower = models.ForeignKey(Profile,related_name='follower')
	followee = models.ForeignKey(Profile,related_name='followee')

	def __str__(self):
		return str(self.follower)+" -> "+str(self.followee)

	class Meta:
		unique_together = (("follower","followee"),)





################################
# Model for topic


class Topic(models.Model):
	text = models.CharField(max_length = 100)
	num_followers = models.IntegerField(default=0)
	num_questions = models.IntegerField(default=0)

	def change_num_followers(self,k=1):
		self.num_followers+=k
		self.save()

	def change_num_questions(self,k=1):
		self.num_questions+=k
		self.save()

	def get_num_followers(self):
		return self.num_followers

	def get_followers(self):
		followers = T_follow.objects.filter(topic=self)
		return followers

	def get_num_questions(self):
		return self.num_questions

	def get_questions(self):
		topic_questions = Related_topic.objects.filter(topic=self)
		questions = []
		for t in topic_questions:
			questions.append(t.get_question())

		return questions


	def __str__(self):
		return str(self.text)


class T_follow(models.Model):
	follower = models.ForeignKey('auth.User')
	topic = models.ForeignKey(Topic)

	def __str__(self):
		return str(self.follower)+" -> "+str(self.topic)

	class Meta:
		unique_together = (("follower","topic"),)









##################################
# Models for question

class Question(models.Model):
	text = models.TextField()
	author = models.ForeignKey('auth.User')
	created_date = models.DateTimeField(default = timezone.now)
	num_followers = models.IntegerField(default=0)
	num_upvotes = models.IntegerField(default=0)

	def change_num_followers(self,k=1):
		self.num_followers+=k
		self.save()

	def change_num_upvotes(self,k=1):
		self.num_upvotes+=k
		self.save()

	def get_num_upvotes(self):
		return self.num_upvotes

	def get_upvotes(self):
		upvotes = Q_upvote.objects.filter(question=self)
		return upvotes

	def get_num_followers(self):
		return self.num_followers

	def get_followers(self):
		followers = Q_follow.objects.filter(question=self)
		return followers

	def get_related_topics(self):
		topics = Related_topic.objects.filter(question=self)
		return topics

	def get_num_answers(self):
		num_answers = Answer.objects.filter(question=self).count()
		return num_answers

	def get_answers(self):
		answers = Answer.objects.filter(question=self).order_by('-created_date')
		return answers

	def get_one_answer(self):
		answers = Answer.objects.filter(question=self).order_by('-created_date')
		answer = None
		if len(answers)>=1:
			answer = answers[0]
		return answer

	
	def __str__(self):
		return self.text

class Q_follow(models.Model):
	follower = models.ForeignKey('auth.User')
	question = models.ForeignKey(Question)

	def __str__(self):
		return str(self.follower)+" -> "+str(self.question)

	class Meta:
		unique_together = (("follower","question"),)


class Q_upvote(models.Model):
	upvoter = models.ForeignKey('auth.User')
	question = models.ForeignKey(Question)

	def __str__(self):
		return str(self.upvoter)+" -> "+str(self.question)


	class Meta:
		unique_together = (("upvoter","question"),)

class Related_topic(models.Model):
	topic = models.ForeignKey(Topic)
	question = models.ForeignKey(Question)

	def get_question(self):
		return self.question

	def __str__(self):
		return str(self.topic)+" <- "+str(self.question)

	class Meta:
		unique_together = (("topic","question"),)




################################

# Models for answers

class Answer(models.Model):
	text = models.TextField()
	author = models.ForeignKey('auth.User')
	created_date = models.DateTimeField(default = timezone.now)
	question = models.ForeignKey(Question)
	num_upvotes = models.IntegerField(default=0)

	def change_num_upvotes(self,k=1):
		self.num_upvotes+=k
		self.save()

	def get_num_upvotes(self):
		return self.num_upvotes

	def get_upvotes(self):
		upvotes = A_upvote.objects.filter(answer=self)
		return upvotes

	def __str__(self):
		return str(self.text)

	class Meta:
		unique_together = (("author","question"),)


class A_upvote(models.Model):
	upvoter = models.ForeignKey('auth.User')
	answer = models.ForeignKey(Answer)


	def get_upvoter(self):
		return self.upvoter

	def __str__(self):
		return str(self.upvoter)+" -> "+str(self.answer)

	class Meta:
		unique_together = (("upvoter","answer"),)







##################################

# Model for Comments

class Comment(models.Model):
	text = models.TextField()
	answer = models.ForeignKey(Answer,null=True)
	author = models.ForeignKey('auth.User')
	created_date = models.DateTimeField(default = timezone.now)
	num_upvotes = models.IntegerField(default=0)

	def change_num_upvotes(self,k=1):
		self.num_upvotes+=k
		self.save()

	def get_num_upvotes(self):
		return self.num_upvotes

	def get_upvotes(self):
		upvotes = C_upvote.objects.filter(comment=self)
		return upvotes

	def get_author(self):
		author = Profile.objects.get(user=self.author)
		return author

	def get_answer(self):
		return self.answer


	def __str__(self):
		return self.text

class C_upvote(models.Model):
	upvoter = models.ForeignKey('auth.user')
	comment = models.ForeignKey(Comment)


	def __str__(self):
		return str(self.upvoter)+" -> "+str(self.comment)

	class Meta:
		unique_together = (("upvoter","comment"),)





############################
# model for profile picture

photos_dir = settings.MEDIA_ROOT + "pictures/"

class Ppic(models.Model):
	ppic = models.ImageField(upload_to = photos_dir,default=photos_dir+"default.jpg")

	def __str__(self):
		return self.ppic.name


