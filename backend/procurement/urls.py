from django.urls import path
from .views import optimize_order

urlpatterns = [
    path('api/optimize-order/', optimize_order),
]
