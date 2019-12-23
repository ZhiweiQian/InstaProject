#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 11:51:56 2019

@author: zhiweiqian
"""


from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from InstaApp.models import InstaUser

# forms defined here handles user inputs

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = InstaUser
        fields = ('username', 'email', 'profile_pic')