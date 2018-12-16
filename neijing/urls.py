from django.urls import path

from .views import *

urlpatterns = [
    path('match/<int:pid>/<int:iid>', match_answer),
    path('exam/<int:pk>', ExamView.as_view())
]
