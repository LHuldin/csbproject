from django import forms
from .models import Note
from django.contrib.auth.models import User

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["content"]
        widgets = {
            "content": forms.TextInput(attrs={
                "placeholder": "Write a note (max 100 characters)",
                "maxlength": 100
            })
        }

    def clean_content(self):
        value = self.cleaned_data["content"].strip()
        if not value:
            raise forms.ValidationError("Note cannot be empty.")
        return value

class TransferNoteForm(forms.Form):
    recipient = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label="Select user to transfer to...",
        widget=forms.Select(attrs={'class': 'form-control'})
    )