from django.urls import path
from . import views

urlpatterns = [
    path('', views.housing_costs_home, name='housing_costs_home'),
    path('Create/', views.housing_costs_create, name='housing_costs_create'),
    path('List/', views.housing_costs_list, name='housing_costs_list'),
    path('Details/<int:pk>/', views.housing_costs_details, name='housing_costs_details'),
    path('Edit/<int:pk>/', views.housing_costs_edit, name='housing_costs_edit'),
    path('Delete/<int:pk>/', views.housing_costs_delete, name='housing_costs_delete'),
    path('ApiData/', views.realty_api_display, name='realty_api_display'),
    path('ApiData/<int:offset>', views.realty_api_display, name='realty_api_display'),
    path('ScrapedData/', views.realty_bs_display, name='realty_bs_display'),
    path('APIError/', views.realty_api_error, name='realty_api_error'),
]
