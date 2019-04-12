#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from shy.utils.unique import unique_id


class Post(models.Model):

    text = models.TextField(default='', blank=False,
                            verbose_name=_(u'text'))

    title = models.CharField(max_length=255, default='', blank=False)

    created_on = models.DateTimeField(auto_now_add=True)

    uuid = models.CharField(unique=True, max_length=50, default=unique_id)

    def __str__(self):
        return u'Post id: {0}'.format(self.id)

    def all_answers(self, obj_type=None):
        if obj_type == 'count':
            return Answers.objects.filter(parent__id=self.id).count()
        return Answers.objects.filter(parent__id=self.id).order_by('created_on')


class Answers(models.Model):

    parent = models.ForeignKey(Post, blank=False, on_delete=models.CASCADE)

    text = models.TextField(default='', blank=True,
                            verbose_name=_(u'text'))

    title = models.CharField(max_length=40, default='', blank=True)

    created_on = models.DateTimeField(auto_now_add=True)

    uuid = models.CharField(unique=True, max_length=50, default=unique_id)

    def __str__(self):
        return u'Post id: {0}'.format(self.id)

    class Meta:
        verbose_name_plural = "Answers"
