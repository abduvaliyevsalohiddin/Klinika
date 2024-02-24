from django.urls import path
from .views import *

urlpatterns = [
    path('xonalar/', XonalarAPI.as_view()),
    path('joylashtirishlar/', JoylashtirishlarAPIView.as_view()),
]
