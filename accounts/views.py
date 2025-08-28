from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin

class SignUpView(SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')
    success_message = 'Your account has been created — please log in.'

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

def home(request):
    return render(request, 'accounts/home.html')