# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Profile, P_follow, Topic, T_follow, Question
from .models import Q_follow, Q_upvote, Related_topic, Answer
from .models import A_upvote, Comment, C_upvote

# Register your models here.

admin.site.register(Profile)
admin.site.register(P_follow)
admin.site.register(Topic)
admin.site.register(T_follow)
admin.site.register(Question)
admin.site.register(Q_follow)
admin.site.register(Q_upvote)
admin.site.register(Related_topic)
admin.site.register(Answer)
admin.site.register(A_upvote)
admin.site.register(Comment)
admin.site.register(C_upvote)