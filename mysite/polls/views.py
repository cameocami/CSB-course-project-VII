from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import Choice, Question, Vote
from .forms import UserCreationForm

class SignupView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'polls/signup.html'
    success_url = '/'

class LoginView(auth_views.LoginView):
    template_name = 'polls/login.html'
    next_page = '/'

class LogoutView(auth_views.LogoutView):
    next_page = '/'

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def sanitize(user_input:str):
    if len(user_input) == 0:
        return "Other"
    if len(user_input) > 200:
        user_input = user_input[:200]
    return user_input

def new_choice(question, choice_text):
    same_text = Choice.objects.filter(choice_text=choice_text)
    if len(same_text) > 0:
        return same_text[0]
    return Choice.objects.create(question=question, choice_text=choice_text)
'''
FLAW 1: Broken Access Control starts here
'''

# @login_required(login_url="/login/") solution to FLAW 1 adds this line
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    if user.is_anonymous:
        user = get_object_or_404(User, pk=1) # solution to FLAW 1 removes this line
        # return HttpResponseRedirect(reverse('polls:login')) solution to FLAW 1 adds this line
    selected_choice = request.POST.get('choice')
    if selected_choice == "other":
        choice_text = sanitize(request.POST.get('new_choice'))
        selected_choice = new_choice(question, choice_text)
    else:
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
    user = request.user
    try:
        Vote.objects.create(user=user, question=question, choice=selected_choice)
    except IntegrityError:
        return render(request, 'polls/results.html', {
            'question': question,
            'error_message': "You have already voted.",
    })
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

'''
FLAW 1: Broken Access Control ends here
'''

'''
FLAW 1: Broken Access Control solution

@login_required(login_url="/login/")
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    if user.is_anonymous:
        return HttpResponseRedirect(reverse('polls:login'))
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })

    try:
        Vote.objects.create(user=user, question=question, choice=selected_choice)
    except IntegrityError:
        return render(request, 'polls/results.html', {
            'question': question,
            'error_message': "You have already voted.",
    })
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

'''
