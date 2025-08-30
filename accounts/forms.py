from django import forms
from .models import Note

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