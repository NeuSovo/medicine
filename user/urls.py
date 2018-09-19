from django.urls import path

from .views import *

urlpatterns = [
    path('reg', RegUserView.as_view()),
    path('login', LoginUserView.as_view()),


    path('case', UserCaseListView.as_view()),
    path('case/<str:case_id>', UserCaseDetailView.as_view())
]
