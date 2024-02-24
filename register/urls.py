from django.urls import path
from .views import *

urlpatterns = [
    path('bemorlar/', BemorlarAPI.as_view()),
    path('yollanmalar/', YollanmalarAPI.as_view()),
]
