import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from polls.models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59,
                                                   seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_future_pub_date(self):
        """
        Test the is_published method with a future pub_date.
        :return False
        """
        future_time = timezone.now() + timezone.timedelta(days=1)
        question = Question(pub_date=future_time)
        self.assertFalse(question.is_published())

    def test_default_pub_date(self):
        """
        Test the is_published method with the default pub_date.
        :return True
        """
        time_now = timezone.now()
        question = Question(pub_date=time_now)
        self.assertTrue(question.is_published())

    def test_past_pub_date(self):
        """
        Test the is_published method with a past pub_date.
        :return True
        """
        past_time = timezone.now() - timezone.timedelta(days=1)
        question = Question(pub_date=past_time)
        self.assertTrue(question.is_published())

    def test_can_vote_with_no_end_date(self):
        """
        Check can_vote when there is no end date set.
        :return True
        """
        time_now = timezone.now()
        question = Question(pub_date=time_now)
        self.assertTrue(question.can_vote())

    def test_can_vote_before_end_date(self):
        """
        Check the can_vote when the current date is before the end date.
        :return True
        """
        time_now = timezone.now()
        end_date = time_now + timezone.timedelta(days=10)
        question = Question(pub_date=time_now, end_date=end_date)
        self.assertTrue(question.can_vote())

    def test_cannot_vote_after_end_date(self):
        """
        Check can_vote when the end date is in the past.
        :return False
        """
        time_now = timezone.now()
        end_date = time_now - timezone.timedelta(days=10)
        question = Question(end_date=end_date)
        self.assertFalse(question.can_vote())

    def test_cannot_vote_before_pub_date(self):
        """
        Check can_vote when the current date is before the pub_date.
        :return False
        """
        time_now = timezone.now()
        pub_date = time_now + timezone.timedelta(days=10)
        question = Question(pub_date=pub_date)
        self.assertFalse(question.can_vote())


def create_question(question_text, days=0, day_end=0):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    if not day_end:
        return Question.objects.create(question_text=question_text,
                                       pub_date=time)
    end_time = time + datetime.timedelta(days=day_end)
    return Question.objects.create(question_text=question_text, pub_date=time,
                                   end_date=end_time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        past_question = create_question("Past Question", days=-5)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/results.html')

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        future_question = create_question("Future Question", days=5)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/results.html')
