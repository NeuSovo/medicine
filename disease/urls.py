from django.urls import path

from .views import *

urlpatterns = [
    path('', DiseaseView.as_view()),
    path('submit', DiseaseSubmit.as_view()),
    path('result', DiseaseResultView.as_view())
]
