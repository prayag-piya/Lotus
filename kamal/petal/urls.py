from django.urls import path
from . import views

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('dns/', views.dns.as_view(), name='DNS'),
    path('rules/', views.rules.as_view(), name='Rule'),
]
