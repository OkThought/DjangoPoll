from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from polls.models import Question


def create_question(text, days):
    """
    Creates and returns a new question in a database with specified text and
    publication date set to (now + specified number of days)
    """
    pub_date = timezone.now() + timezone.timedelta(days=days)
    return Question.objects.create(question_text=text, pub_date=pub_date)


class IndexViewTests(TestCase):

    def test_no_questions(self):
        """
        If no questions exist an appropriate message is displayed
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)  # OK
        self.assertContains(response, 'No polls are available.')
        self.assertFalse(response.context['latest_questions'])

    def test_past_question(self):
        """
        Questions with publication date in the past displayed in index
        """
        past_questions = [
            create_question(text='past question', days=-30),
        ]
        response = self.client.get(reverse('polls:index'))
        self.assertListEqual(list(response.context['latest_questions']),
                             past_questions)

    def test_future_question(self):
        """
        Questions with publication date in the future not displayed in index
        """
        create_question(text='future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertFalse(response.context['latest_questions'])

    def test_past_question_and_future_question(self):
        """
        Even if both type of questions exist, only the past are displayed
        """
        past_questions = [
            create_question(text='past question', days=-30),
        ]
        create_question(text='future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertListEqual(list(response.context['latest_questions']),
                             past_questions)

    def test_two_past_questions(self):
        """
        Index page is able to display multiple questions
        """
        questions = [
            create_question(text='past question 1', days=-29),
            create_question(text='past question 2', days=-30),
        ]
        response = self.client.get(reverse('polls:index'))
        self.assertListEqual(
            list(response.context['latest_questions']),
            questions
        )


class QuestionDetailTests(TestCase):

    def test_future_question(self):
        """
        An attempt to get a detail view of a question with future publication
        date results in '404 Page Not Found'
        """
        future_question = create_question(text='future question', days=+30)
        response = self.client.get(reverse('polls:detail',
                                           args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)  # Page Not Found

    def test_past_question(self):
        """
        Detail view of a question with past publication date displays the
        question's text
        """
        question = create_question(text='past question', days=-30)
        response = self.client.get(reverse('polls:detail', args=(question.id,)))
        self.assertEqual(response.status_code, 200)  # OK
        self.assertContains(response, question.question_text)


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
