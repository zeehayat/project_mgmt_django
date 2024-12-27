from django.contrib import admin
from .models import ProjectUser, Project, Task, Notification, UserCommunicationChannel, Role, ProjectMember, UserRole

admin.site.register(ProjectUser)
admin.site.register(Role)
#admin.site.register(Project)
admin.site.register(ProjectMember)
#admin.site.register(Task)
admin.site.register(UserRole)
admin.site.register(Notification)
admin.site.register(UserCommunicationChannel)


@admin.register(Project)  # Use a decorator for cleaner syntax
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'start_date', 'due_date', 'status')
    list_filter = ('status',)  # Add filters
    search_fields = ('name', 'description')  # Add search fields

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'assignee', 'due_date', 'status')
    list_filter = ('status', 'priority')
    search_fields = ('name', 'description')