# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Topic(models.Model):
	topic = models.CharField(max_length = 100)


	def __str__(self):
		return str(self.topic)


class T_follow(models.Model):
	follower = models.ForeignKey('auth.User')
	topic = models.ForeignKey(Topic)

	def __str__(self):
		return str(self.follower)+" -> "+str(self.topic)

	class Meta:
		unique_together = (("follower","topic"),)
