from django.urls import path
from . import views

urlpatterns = [
    # Regular user endpoints
    path('api/submit/', views.submit_request, name='submit_request'),
    path('api/track/', views.track_requests, name='track_requests'),
    
    # Admin endpoints
    path('api/admin/requests/', views.admin_list_requests, name='admin_list_requests'),
    path('api/admin/requests/<int:request_id>/', views.admin_request_detail, name='admin_request_detail'),
]

