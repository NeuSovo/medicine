from django.urls import path

from .views import *

urlpatterns = [
    path('', DiseaseView.as_view()),
]
