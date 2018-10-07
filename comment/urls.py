from django.urls import path

from .views import *

urlpatterns = [
    path('<int:disease_id>', CommentView.as_view()),
]
