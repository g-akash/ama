# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.


class Topic(models.Model):
	topic = models.CharField(max_length = 100)

	# def get_num_followers(self):
	# 	num_followers = T_follow.objects.filter(topic=self).count()
	# 	return num_followers

	# def get_followers(self):
	# 	followers = T_follow.objects.filter(topic=self)
	# 	return followers

	# def get_num_questions(self):
	# 	num_questions = Related_topic.objects.filter(topic=self).count()
	# 	return num_questions

	# def get_questions(self):
	# 	topic_questions = Related_topic.objects.filter(topic=self)
	# 	questions = []
	# 	for t in topic_questions:
	# 		questions.append(t.get_question())

	# 	return questions


	def __str__(self):
		return str(self.topic)


class T_follow(models.Model):
	follower = models.ForeignKey('auth.User')
	topic = models.ForeignKey(Topic)

	def __str__(self):
		return str(self.follower)+" -> "+str(self.topic)

	class Meta:
		unique_together = (("follower","topic"),)
