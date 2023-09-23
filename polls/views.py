from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
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
                                       ).order_by('-pub_date')


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
            question = get_object_or_404(Question, pk=kwargs['pk'])
        except (Question.DoesNotExist,Http404):
            messages.error(request,
                           f"Poll number {kwargs['pk']} does not exist.")
            return redirect("polls:index")

        this_user = request.user
        try:
            prev_vote = Vote.objects.get(user=this_user,
                                         choice__question=question)
        except (Vote.DoesNotExist, TypeError):
            prev_vote = None

        if not question.can_vote():
            messages.error(request, f"Poll question {kwargs['pk']} "
                                    f"is not allow to voting.")
            return redirect("polls:index")
        else:
            return render(request, self.template_name,
                          {"question": question,
                           "prev_vote": prev_vote})


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# need import \/
@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if not question.can_vote():
        messages.error(request, f"poll number {question.id}"
                                f" is not available to vote.")
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
    try:
        """find a vote for this user and this question"""
        vote = Vote.objects.get(user=this_user, choice__question=question)
        # update his vote
        vote.choice = selected_choice
    except Vote.DoesNotExist:
        vote = Vote(user=this_user, choice=selected_choice)

    vote.save()
    messages.success(request,
                     f'Your last vote is {selected_choice.choice_text}'
                     f' has been saved.')

    return HttpResponseRedirect(
        reverse('polls:results', args=(question.id,)))
