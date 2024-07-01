# payments/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_payment, name='start_payment'),
    path('return/', views.return_from_payment, name='return_from_payment'),
    path('finalize/', views.finalize_payment, name='finalize_payment'),
    path('button/', views.payment_button, name='payment_button'),
]
