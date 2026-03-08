from django.urls import path
from .views import generate_token
from sqms.queue_system import views

urlpatterns = [

    # Token generation API
    path('generate-token/', generate_token, name='generate_token'),
    # Service APIs
    path('services/', views.service_list),
    path('services/<int:pk>/', views.service_detail),
    path('services/create/', views.service_create),
    path('services/update/<int:pk>/', views.service_update),
    path('services/delete/<int:pk>/', views.service_delete),
    # Counter APIs
    path('counters/', views.counter_list),
    path('counters/<int:pk>/', views.counter_detail),
    path('counters/create/', views.counter_create),
    path('counters/update/<int:pk>/', views.counter_update),
    path('counters/delete/<int:pk>/', views.counter_delete),
]