from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()
                                       ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """
        Handles the HTTP GET request for the poll detail page.
        """
        try:
            self.question = self.get_object()
        except Exception:
            messages.error(request,
                           f"Poll number {kwargs['pk']} does not exist.")
            return redirect("polls:index")
        else:
            if not self.question.can_vote():
                messages.error(request,
                               f"Poll number {kwargs['pk']} not allow voting.")
                return redirect("polls:index")
            else:
                return super().get(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# need import \/
@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if not question.can_vote():
        messages.error(request, f"poll number {question.id}"
                                f"is not available to vote.")
        return redirect("polls:index")

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })

    this_user = request.user
    # selected_choice.votes += 1
    # selected_choice.save()
    try:
        """find a vote for this user and this question"""
        vote = Vote.objects.get(user=this_user, choice__question=question)
        # update his vote
        vote.choice = selected_choice
    except Vote.DoesNotExist:
        vote = Vote(user = this_user,choice = selected_choice)

    vote.save()
        # TODO:use messages to display a confirmation on the results page.

    return HttpResponseRedirect(
        reverse('polls:results', args=(question.id,)))
