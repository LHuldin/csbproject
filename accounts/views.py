# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .forms import NoteForm
from .models import Note

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

@login_required
def notes(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, "Note saved.")
            return redirect("notes")
    else:
        form = NoteForm()

    user_notes = request.user.notes.all()
    return render(request, "accounts/notes.html", {"form": form, "notes": user_notes})