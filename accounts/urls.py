from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import SignUpView, profile, home, notes, transfer_note, logout_view

urlpatterns = [
    path('', home, name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', profile, name='profile'),
    path('notes/', notes, name='notes'),
    path('transfer/<int:note_id>/', transfer_note, name='transfer_note'),
    path('logout/', logout_view, name='logout'),
]


