# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .forms import NoteForm, TransferNoteForm
from .models import Note
from django.views.decorators.csrf import csrf_exempt

def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')

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

# CSRF VULNERABILITY: @csrf_exempt disables CSRF protection
# FIX: Remove @csrf_exempt decorator below
@csrf_exempt
@login_required
def transfer_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    # A01 VULNERABILITY: No ownership verification - any user can transfer any note
    # FIX: Add ownership check before allowing transfer:
    # if note.user != request.user:
    #     messages.error(request, "You can only transfer your own notes")
    #     return redirect('notes')
    
    if request.method == 'POST':
        form = TransferNoteForm(request.POST)
        if form.is_valid():
            note.user = form.cleaned_data['recipient']
            note.save()
            messages.success(request, f"Note transferred to {note.user.username}")
            return redirect('notes')
    else:
        form = TransferNoteForm()
    
    return render(request, 'accounts/transfer_note.html', {
        'form': form, 
        'note': note
    })