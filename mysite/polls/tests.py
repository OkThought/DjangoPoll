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
