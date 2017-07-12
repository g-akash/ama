# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from Question.models import Question
from Answer.models import Answer
# Create your models here.


class Comment(models.Model):
	text = models.TextField()
	answer = models.ForeignKey(Answer,null=True)
	question = models.ForeignKey(Question,null=True)
	author = models.ForeignKey('auth.User')
	created_date = models.DateTimeField(default = timezone.now)

	


	def __str__(self):
		return self.text

class C_upvote(models.Model):
	upvoter = models.ForeignKey('auth.user')
	comment = models.ForeignKey(Comment)


	def __str__(self):
		return str(self.upvoter)+" -> "+str(self.comment)

	class Meta:
		unique_together = (("upvoter","comment"),)