#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def mark(request):
    """
    ��ǣ��൱���ղ�
    ͨ�� Ajax ��ʽ���� POST ����
        content_type: 'question' / 'answer'
        object_pk: '...'
    """
    if request.method == 'POST':
        return HttpResponse('')
    return HttpResponse('')

@login_required
def unmark(request):
    """
    ȡ�����
    ͨ�� Ajax ��ʽ���� POST ����
        content_type: 'question' / 'answer'
        object_pk: '...'
    """
    if request.method == 'POST':
        return HttpResponse('')
    return HttpResponse('')

def marked(request, user_id):
    """
    ��ȡ�û����ղ��б�
    ͨ�� Ajax ��ʽ���� POST ����
        content_type: 'question' / 'answer'
    """
    return HttpResponse('')