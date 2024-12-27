from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('roles/', views.RoleListCreateView.as_view(), name='role-list-create'),
    path('projects/', views.ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', views.ProjectRetrieveUpdateDestroyView.as_view(), name='project-retrieve-update-destroy'),
    path('project_members/', views.ProjectMemberListCreateView.as_view(), name='project_member-list-create'),
    path('project_members/<int:pk>/', views.ProjectMemberRetrieveUpdateDestroyView.as_view(), name='project_member-retrieve-update-destroy'),
    path('tasks/', views.TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', views.TaskRetrieveUpdateDestroyView.as_view(), name='task-retrieve-update-destroy'),
    path('user_roles/', views.UserRoleListCreateView.as_view(), name='user_role-list-create'),
    path('notifications/', views.NotificationListCreateView.as_view(), name='notification-list-create'),
    path('user_communication_channels/', views.UserCommunicationChannelListCreateView.as_view(), name='user_communication_channel-list-create'),

    path('api-token-auth/', views.CustomAuthToken.as_view()),  # Add this line

    path('memb/',views.CurrentDateTime,name='memb'),

]