#-*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from zhidewen.models import base
from zhidewen.models.tag import Tag


class QuestionQuerySet(base.QuerySet):

    def fresh(self):
        return self.order_by('-last_refreshed_at')

    def hot(self):
        return self.order_by('-ranking_weight')

    def unanswered(self):
        return self.filter(answer_count=0, closed=False).order_by('-created_at')


class QuestionManager(QuestionQuerySet.as_manager()):

    def create_question(self, user, title, content, **kwargs):
        return self.create(title=title, content=content, created_by=user, last_updated_by=user, **kwargs)


class Question(base.ContentModel):
    objects = QuestionManager()
    existed = QuestionManager.existed_manager()

    title = models.CharField(max_length=140, verbose_name=u'标题')
    content = models.TextField(verbose_name=u'补充说明', null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name=u'标签')

    view_count = models.PositiveIntegerField(default=0, verbose_name=u'浏览数')
    answer_count = models.PositiveIntegerField(default=0, verbose_name=u'回答数')

    last_refreshed_at = models.DateTimeField(auto_now_add=True, verbose_name=u'最后活跃时间')
    closed = models.BooleanField(default=False, verbose_name=u'是否被关闭')


    class Meta:
        app_label = 'zhidewen'
        db_table = 'zhidewen_questions'

    def count_ranking(self):
        return sum([self.answer_count*5,
                    self.up_count*3,
                    self.mark_count*2,
                    self.down_count,
                    self.view_count,
                    self.comment_count])

    def update(self, user, title, content):
        self.title = title
        self.content = content
        self.last_updated_by = user
        self.last_updated_at = timezone.now()
        return self.save()
