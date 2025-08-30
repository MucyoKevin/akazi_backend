from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.ServiceCategoryListView.as_view(), name='service_categories'),
    path('', views.ServiceListView.as_view(), name='services'),
    path('<int:pk>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('<int:service_id>/packages/', views.service_packages, name='service_packages'),
    path('<int:service_id>/providers/', views.service_providers, name='service_providers'),
    path('featured-providers/', views.featured_providers, name='featured_providers'),
]
