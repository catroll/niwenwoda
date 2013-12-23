#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages import *
from zhidewen.models import User
from zhidewen.forms import LoginForm, RegisterForm


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # ��֤
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                # ����Ñ������L��ĳ���ĕr�����D�^��ģ���ꑳɹ�֮���Ԅ��D��֮
                # ǰ�L������档
                next_url = request.GET.get('next', reverse('index'))
                return HttpResponseRedirect(next_url)
            error(request, u'��Ǹ������ͨ����֤��')
    else:
        form = LoginForm()

    content = {
        'form': form,
        'title': u'��¼',
    }

    return render_to_response('users/login.html', content,
                              context_instance=RequestContext(request))

@login_required
def logout(request):
    """
    �˳���ת���¼ҳ��
    """
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username, email, password)
            user.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegisterForm()

    content = {
        'form': form,
        'title': u'ע��',
    }

    return render_to_response('accounts/register.html', content,
                              context_instance=RequestContext(request))

def wall(request):
    """
    �û�ǽҳ��
    """
    users = User.objects.filter(is_active=True).order_by('-reputation')
    content = {'users': users}
    return render_to_response('users/index.html', content,
                              context_instance=RequestContext(request))

def home(request, username):
    """
    �û���ҳ
    eg: /u/catroll
    """
    user = User.objects.get(username=username)
    return render(request, 'users/show.html', {'user': user})

@login_required
def change_profile(request):
    """
    �޸ĸ�����Ϣ
    """
    return HttpResponse('')

@login_required
def change_password(request):
    """
    �޸�����
    """
    return HttpResponse('')


@login_required
def most_prestigious(request):
    """
    ���� 15 �������������û�
    """
    users = User.objects.filter(is_active=True).order_by('-reputation')[:10]
    return HttpResponse(json.dumps({}))

def contents(request, username, template):
    user = User.objects.get(username=username)
    return render(request, template, {'user': user })

def _list(qs):
    return {}

def _item(instance):
    return {}
