from django.urls import path

from .views import *

urlpatterns = [
    path('match/<int:pid>/<int:iid>', match_answer),
    path('list', NeiJingList.as_view()),
    path('exam/<int:pk>', ExamView.as_view()),
    path('exam/detail/<int:pk>', ExamDetailView.as_view())
]
