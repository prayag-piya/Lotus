from django.urls import path
from . import views

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('dns/', views.dns.as_view(), name='DNS'),
    path('network/', views.network.as_view(), name='Network'),
    path('rules/', views.rules.as_view(), name='Rule'),
    path('add_plan/', views.plan.as_view(), name='Add Plan'),
]
