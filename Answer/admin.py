# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Answer, A_upvote

# Register your models here.

admin.site.register(Answer)
admin.site.register(A_upvote)
