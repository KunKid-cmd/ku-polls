import datetime

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """ attribute of a question in a poll."""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField('date ended', default=None, null=True,
                                    blank=True)

    def __str__(self):
        """Returns a string of the question."""
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        """to check is the polls published date within last day."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """
        To check if the question is published.
        :return:
        True if the current date is on or after question’s publication date
        """
        return timezone.now() >= self.pub_date

    def can_vote(self):
        """
        to check if question allow to vote
        :return: True if voting is allowed for this question,
                 False otherwise.
        """
        now = timezone.now()
        if self.end_date is None:
            return now >= self.pub_date
        return self.pub_date <= now <= self.end_date


class Choice(models.Model):
    """ Represents a choice in the poll question."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    # votes = models.IntegerField(default=0)

    @property
    def votes(self):
        """count the votes for this choice."""
        # count = Vote.objects.filter(choice=self).count()
        return self.vote_set.count()

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    """Record vote of a choice by a user"""
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
