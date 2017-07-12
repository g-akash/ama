# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Profile(models.Model):
	user = models.ForeignKey('auth.User')

	# def get_num_followers(self):
	# 	num_followers = P_follow.objects.filter(followee=self).count()
	# 	return num_followers

	# def get_followers(self):
	# 	followers = P_follow.objects.filter(followee=self)
	# 	return followers

	# def get_num_followees(self):
	# 	num_followees = P_follow.objects.filter(follower=self).count()
	# 	return num_followees

	# def get_followees(self):
	# 	followees = P_followees.objects.filter(follower=self)
	# 	return followees

	# def get_num_questions(self):
	# 	num_questions = Question.objects.filter(author=self.user).count()
	# 	return num_questions

	# def get_questions(self):
	# 	questions = Question.objects.filter(author=self.user)
	# 	return questions


	# def getQandA(self):
	# 	questions = Question.objects.filter(author=self.user)
	# 	answers = []
	# 	for question in questions:
	# 		answer = Answer.objects.filter(author=self,question=question)
	# 		answers.append(answer)

	# 	return questions, answers


	def __str__(self):
		return str(self.user)

	class Meta:
		unique_together = (("user"),)




class P_follow(models.Model):
	follower = models.ForeignKey('auth.User',related_name='follower')
	followee = models.ForeignKey('auth.User',related_name='followee')

	def __str__(self):
		return str(self.follower)+" -> "+str(self.followee)

	class Meta:
		unique_together = (("follower","followee"),)
