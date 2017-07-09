# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Profile(models.Model):
	user = models.ForeignKey('auth.User')


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
