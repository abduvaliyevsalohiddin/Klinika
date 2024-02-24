from django.urls import path
from .views import *

urlpatterns = [
    path('hammasi/', TolovlarAPIView.as_view()),
    path('admin_uchun/', TolovlarAdminAPIView.as_view()),
    path('qoshimcha_tolovlar/', QoshimchaTolovlarAPIView.as_view()),
    path('tolov/<int:pk>/', TolovAPIView.as_view()),
]
