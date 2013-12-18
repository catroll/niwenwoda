#-*- encoding: utf-8 -*-

from django.test import TestCase
from zhidewen.models import Vote, Question, User, Mark
from zhidewen.tests.models.base import ModelTestCase


class TestMark(ModelTestCase):

    def setUp(self):
        self.user = self.create_user('test')
        self.q = self.create_question(self.user, 'Foo', 'Bar')

    def test_add_and_delete_mark(self):
        mark = Mark.objects.mark(self.user, self.q)

        self.assertEqual(self.reload(self.q).mark_count, 1)
        self.assertEqual(self.reload(mark).content_object, self.q)

        mark = Mark.objects.mark(self.user, self.q)
        self.assertEqual(self.reload(self.q).mark_count, 1)

        mark.delete()
        self.assertEqual(self.reload(self.q).mark_count, 0)

