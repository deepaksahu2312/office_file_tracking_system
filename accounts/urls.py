from django.urls import re_path
from django.urls import path

from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'student/register/$', views.UserFormView.as_view(), name='student_register'),
    re_path(r'staff/register/$', views.StaffFormView.as_view(), name='staff_register'),
    re_path(r'login/$', views.user_login, name='login'),
    re_path(r'logout/$', views.user_logout, name='logout'),
    re_path(r'getNames/', views.getNames),
    path('activate_users/', views.Activate_Users, name='Activate_Users'),
    path('activate/<int:uid>', views.Activate, name='Activate'),
    path('deactivate/<int:uid>', views.Deactivate, name='Deactivate'),
]
