# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Question, Q_follow, Q_upvote, Related_topic

# Register your models here.

admin.site.register(Question)
admin.site.register(Q_follow)
admin.site.register(Q_upvote)
admin.site.register(Related_topic)