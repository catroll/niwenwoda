#-*- encoding: utf-8 -*-

from django.test import TestCase
from zhidewen.models import Question, User
import datetime

class BaseQuestionTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('test', 'test@zhidewen.com', 'test')

    def create(self, *args, **kwargs):
        return Question.objects.create_question(self.user, *args, **kwargs)


class TestQuestion(BaseQuestionTest):

    def test_create_question(self):
        question = Question.objects.create_question(self.user, 'Foo', 'Bar')

        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(list(self.user.questions.all()), [question])

    def test_count_ranking_when_create_or_update_question(self):
        question = self.create('Foo', 'Bar', view_count=100, answer_count=5)

        self.assertEqual(question.ranking_weight, 125)

        question.view_count += 10
        question.answer_count += 1
        question.save()
        self.assertEqual(question.ranking_weight, 140)


class TestListQuestion(BaseQuestionTest):

    def setUp(self):
        super(TestListQuestion, self).setUp()
        self.q1 = self.create('Q1', 'Q1', answer_count=1)
        self.q2 = self.create('Q2', 'Q2', view_count=100)
        self.q3 = self.create('Q3', 'Q3')

        self.q2.last_refreshed_at = datetime.datetime.now()
        self.q2.save()

    def test_fresh_list(self):
        self.assertEqual(list(Question.objects.fresh()), [self.q2, self.q3, self.q1])

    def test_hot_list(self):
        self.assertEqual(list(Question.objects.hot()), [self.q2, self.q1, self.q3])

    def test_unanswered_list(self):
        self.assertEqual(list(Question.objects.unanswered()), [self.q3, self.q2])

        self.q3.closed = True
        self.q3.save()

        self.assertEqual(list(Question.objects.unanswered()), [self.q2])

