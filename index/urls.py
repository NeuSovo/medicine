from django.urls import path

from .views import *

urlpatterns = [
    path('lunbo', get_lunbo_img),
    path('index', IndexList.as_view()),
    path('baike', BaikeView.as_view())
]
