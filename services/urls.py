from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.ServiceCategoryListView.as_view(), name='service_categories'),
    path('', views.ServiceListView.as_view(), name='services'),
    path('featured-providers/', views.featured_providers, name='featured_providers'),
]
