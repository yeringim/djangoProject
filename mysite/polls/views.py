from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from polls.models import Question, Choice
from polls.forms import NameForm

from django.views.generic import ListView
from django.views.generic import DetailView

import logging
logger = logging.getLogger(__name__)


# def index(request):
#     latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)
class IndexView(ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]



# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
class DetailView(DetailView):
    model = Question
    template_name = 'polls/detail.html'



def vote(request, question_id):
    logger.debug(f"vote().question_id: {question_id}")
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
class ResultsView(DetailView):
    model = Question
    template_name = 'polls/results.html'



def name(request):
    form = NameForm(request.POST)

    if request.method == 'POST':

        if form.is_valid():
            new_name = form.cleaned_data['name']
            return HttpResponseRedirect('')
        else:
            form = NameForm()
    return render(request, 'polls/name.html', {'form': form})