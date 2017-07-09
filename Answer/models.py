# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from Question.models import Question

# Create your models here.


class Answer(models.Model):
	text = models.TextField()
	author = models.ForeignKey('auth.User')
	created_date = models.DateTimeField(default = timezone.now)
	question = models.ForeignKey(Question)

	def __str__(self):
		return str(self.text)

	def get_num_upvotes(self):
		num_upvotes = A_upvote.objects.filter(answer=self).count()
		return num_upvotes

	class Meta:
		unique_together = (("author","question"),)


class A_upvote(models.Model):
	upvoter = models.ForeignKey('auth.User')
	answer = models.ForeignKey(Answer)

	def __str__(self):
		return str(self.upvoter)+" -> "+str(self.answer)

	class Meta:
		unique_together = (("upvoter","answer"),)

