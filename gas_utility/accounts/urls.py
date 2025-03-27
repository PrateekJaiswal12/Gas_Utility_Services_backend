from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', views.register, name='api_register'),
    path('api/login/', views.login_view, name='api_login'),
    path('api/account/', views.account_info, name='api_account'),
    
    path('api/admin/users/', views.admin_list_users, name='admin_list_users'),
    path('api/admin/users/create/', views.admin_create_user, name='admin_create_user'),
    path('api/admin/users/<int:user_id>/', views.admin_user_detail, name='admin_user_detail'),
]
