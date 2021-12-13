from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView

from accountapp.models import NewModel


def hello_world(request):

    if request.method == 'POST':
        input_data = request.POST.get('input_data')

        new_model = NewModel()
        new_model.text = input_data
        new_model.save()

        return HttpResponseRedirect(reverse('accountapp:hello_world'))

    new_model_list = NewModel.objects.all()
    return render(request, 'accountapp/hello_world.html',
                  context={'new_model_list': new_model_list})


class AccountCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'accountapp/create.html'


class AccountDetailView(DetailView):
    model = User
    context_object_name = 'target_user'
    template_name = 'accountapp/detail.html'

