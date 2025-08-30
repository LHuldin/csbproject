from django.urls import path
from .views import SignUpView, profile, home, notes, transfer_note

urlpatterns = [
    path('', home, name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', profile, name='profile'),
    path('notes/', notes, name='notes'),
    path('transfer/<int:note_id>/', transfer_note, name='transfer_note'),
]


