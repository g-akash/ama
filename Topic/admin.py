# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Topic, T_follow


# Register your models here.

admin.site.register(Topic)

admin.site.register(T_follow)
