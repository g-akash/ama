# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Comment, C_upvote


# Register your models here.

admin.site.register(Comment)
admin.site.register(C_upvote)
