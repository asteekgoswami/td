from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task
# Create your views here.


@csrf_exempt
class CustomLoginView(LoginView):
    template_name='base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return  reverse_lazy('tasks')

@csrf_exempt
class RegisterPage(FormView):
    template_name='base/register.html'
    form_class=UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form) :
        user=form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage,self).get(*args,**kwargs)


@csrf_exempt
class TaskList(LoginRequiredMixin,ListView):
    model=Task
    context_object_name="tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        context['count']=context['tasks'].filter(complete=False).count()

        search_input=self.request.GET.get("Search_Area") or ''
        if search_input:
            context['tasks']=context['tasks'].filter(title__startswith=search_input)
        
        context['search_input']=search_input
        return context


@csrf_exempt
class TaskDetail(DetailView):
    model=Task
    context_object_name='task'
    template_name='base/task.html'


@csrf_exempt
class TaskCreate(CreateView):
    model=Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)


@csrf_exempt
class TaskUpdate(UpdateView):
    model=Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')


@csrf_exempt
class DeleteView(DeleteView):
    model=Task
    context_object_name="task"
    success_url = reverse_lazy('tasks')
