from django.urls import path
from . import views

urlpatterns = [
    path('tenant_view/', views.tenant_view, name='tenant_view'),
]
