from django.urls import path
from . import views

urlpatterns = [
     path('', views.login_view, name='login'),
     path('user-home/', views.home, name='home'),
    path('my-tasks/', views.my_tasks, name='my_tasks'),
    path('complete-task/<int:task_id>/', views.complete_task, name='complete_task'),
     path('completed-task/<int:task_id>/', views.view_completed_task, name='view_completed_task'),
      path('view-report/<int:task_id>/', views.view_report, name='view_report'),
      path('admin-home/', views.admin_home, name='admin_home'),
      path("assign-task/", views.assign_task, name="assign_task"),
      path('superadmin/', views.superadmin_home, name='superadmin_home'),
      path('reports/', views.all_reports, name='all_reports'),
      path('assign-task/', views.assign_task, name='assign_task'),
      path("superadmin/manage-admin/", views.manage_admin_view, name="manage_admin"),
      
      path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('reset-password/', views.password_reset_request, name='password_reset_request'),
    path('reset-password/new/', views.password_reset_new, name='password_reset_new'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('superadmin/tasks/', views.superadmin_task_management, name='superadmin_task_management'),
    path('admin-home/my-assigned-tasks/', views.admin_assigned_tasks, name='admin_assigned_tasks'),
    path('superadmin/all-users/', views.all_users_view, name='all_users'),
    path('superadmin/delete-user/', views.delete_user_view, name='delete_user')





    
    
]


