from django.urls import path

from .views import *

urlpatterns = [
    path('reg', RegUserView.as_view()),
    path('login', LoginUserView.as_view()),
]
