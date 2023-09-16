"""Tests of authentication."""
import django.test
from django.urls import reverse
from django.contrib.auth.models import User
from polls.models import Question, Choice
from mysite import settings


class UserAuthTest(django.test.TestCase):

    def setUp(self):
        """ Tests authentication for user. """
        super().setUp()
        self.username = "AuthenUser"
        self.password = "UserName01"
        self.user1 = User.objects.create_user(
            username=self.username,
            password=self.password,
            email="testuser@nowhere.com"
        )
        self.user1.first_name = "Authen"
        self.user1.save()
        q = Question.objects.create(question_text="First Poll Question")
        q.save()
        for n in range(1, 4):
            choice = Choice(choice_text=f"Choice {n}", question=q)
            choice.save()
        self.question = q

    def test_logout(self):
        """Check user can log out using url."""
        logout_url = reverse("logout")
        self.assertTrue(
              self.client.login(username=self.username,
                                password=self.password))
        response = self.client.get(logout_url)
        self.assertEqual(302, response.status_code)

        self.assertRedirects(response, reverse(settings.LOGOUT_REDIRECT_URL))

    def test_login(self):
        """Check user can log in using the login view."""
        login_url = reverse("login")
        response = self.client.get(login_url)
        self.assertEqual(200, response.status_code)
        form_data = {"username": "AuthenUser",
                     "password": "UserName01"
                     }
        response = self.client.post(login_url, form_data)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

    def test_auth_required_to_vote(self):
        """Check authentication is required to submit a vote."""
        vote_url = reverse('polls:vote', args=[self.question.id])
        choice = self.question.choice_set.first()
        form_data = {"choice": f"{choice.id}"}
        response = self.client.post(vote_url, form_data)
        self.assertEqual(response.status_code, 302)
        login_with_next = f"{reverse('login')}?next={vote_url}"
        self.assertRedirects(response, login_with_next)