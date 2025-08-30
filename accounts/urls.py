from django.urls import path
from .views import SignUpView, profile, home, notes

urlpatterns = [
    path('', home, name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', profile, name='profile'),
    path('notes/', notes, name='notes'),
]


