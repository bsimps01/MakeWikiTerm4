from . import views
from django.urls import path, include

urlpatterns = [
    path('SignUp/', views.SignUpView.as_view()),
]