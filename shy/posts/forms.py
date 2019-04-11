#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from django import forms
from django.forms.widgets import TextInput

from shy.posts.models import Answers, Post


class AnswersForm(forms.ModelForm):

    title = forms.CharField(error_messages={'invalid': 'Επιτρέπονται μόνο γράμματα και αριθμοί.'},
                            required=False,
                            max_length=40,
                            widget=TextInput(attrs={
                                'class': 'form-control input-sm',
                                'required': 'False',
                                'placeholder': 'Τίτλος'}))

    text = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'form-control ',
        'rows': '3',
        'required': 'True',
        'placeholder': 'Κείμενο'}
    ))

    # parent = forms.ModelChoiceField(queryset=Post.objects.all())

    def clean_title(self):
        """Ensure that title is valid."""
        data = self.cleaned_data['title']
        if not re.match(r'(^[\w\s.-]+$)', data, re.UNICODE):
            raise forms.ValidationError(
                u'Επιτρέπονται μόνο γράμματα και αριθμοί.')
        return data

    def clean_text(self):
        data = self.cleaned_data['text']
        text = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", data)
        return text

    class Meta:
        model = Answers
        fields = ('text', 'title')
        # fields = '__all__'


class PostForm(forms.ModelForm):

    title = forms.CharField(error_messages={'invalid': 'Επιτρέπονται μόνο γράμματα και αριθμοί.'},
                            required=True,
                            max_length=40,
                            widget=TextInput(attrs={
                                'class': 'form-control input-sm',
                                'required': 'True',
                                'placeholder': 'Τίτλος'}))

    text = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'form-control ',
        'rows': '3',
        'required': 'True',
        'placeholder': 'Κείμενο'}
    ))

    # parent = forms.ModelChoiceField(queryset=Post.objects.all())

    def clean_title(self):
        """Ensure that title is valid."""
        data = self.cleaned_data['title']
        if not re.match(r'(^[\w\s.-]+$)', data, re.UNICODE):
            raise forms.ValidationError(
                u'Επιτρέπονται μόνο γράμματα και αριθμοί.')
        return data

    def clean_text(self):
        data = self.cleaned_data['text']
        text = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", data)
        return text

    class Meta:
        model = Post
        fields = ('text', 'title')
        # fields = '__all__'
