#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from shy.utils.unique import unique_id


class Post(models.Model):

    text = models.TextField(default='', blank=False,
                            verbose_name=_(u'text'))

    title = models.CharField(max_length=255, default='', blank=False,
                             verbose_name=_(u'Mount name'))

    created_on = models.DateTimeField(auto_now_add=True)

    uuid = models.CharField(unique=True, max_length=50, default=unique_id)


    def __str__(self):
        return u'Post id: {0}'.format(self.id)

