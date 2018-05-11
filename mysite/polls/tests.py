from django.test import TestCase
from django.utils import timezone

from polls.models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        Question's was_published_recently returns False for a
        question with future pub_date
        """
        future_time = timezone.now() + timezone.timedelta(days=30)
        future_question = Question(pub_date=future_time)
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for a question
        with pub_date within one day the past
        """
        for step_back in [
            timezone.timedelta(hours=23, minutes=59, seconds=59),
            timezone.timedelta(hours=12),
            timezone.timedelta(seconds=1),
            timezone.timedelta(seconds=0),
        ]:
            past_time = timezone.now() - step_back
            past_question = Question(pub_date=past_time)
            self.assertTrue(past_question.was_published_recently())

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for a question
        with pub_date older than one day the past
        """
        for step_back in [
            timezone.timedelta(days=1, seconds=1),
            timezone.timedelta(days=2),
        ]:
            past_time = timezone.now() - step_back
            past_question = Question(pub_date=past_time)
            self.assertFalse(past_question.was_published_recently())
