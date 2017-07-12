# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from Topic.models import Topic
#from Answer.models import Answer

# Create your models here.

class Question(models.Model):
	text = models.TextField()
	author = models.ForeignKey('auth.User')
	created_date = models.DateTimeField(default = timezone.now)

	def get_num_upvotes(self):
		num_upvotes = Q_upvote.objects.filter(question=self).count()
		return num_upvotes

	def get_upvotes(self):
		upvotes = Q_upvote.objects.filter(question=self)
		return upvotes

	def get_num_followers(self):
		num_followers = Q_follow.objects.filter(question=self).count()
		return num_followers

	def get_followers(self):
		followers = Q_follow.objects.filter(question=self)
		return followers

	def get_related_topics(self):
		topics = Related_topic.objects.filter(question=self)
		return topics

	# def get_num_answers(self):
	# 	num_answers = Answer.objects.filter(question=self).count()
	# 	return num_answers

	# def get_answers(self):
	# 	answers = Answer.objects.filter(question=self).order_by('-created_date')
	# 	return answers

	
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