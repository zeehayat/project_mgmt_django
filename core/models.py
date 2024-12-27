from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class ProjectUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20, blank=True)  # Adjust data type and null settings as needed
    REQUIRED_FIELDS = [ 'password', 'email']

    def __str__(self):
        return self.username

class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # CRUCIAL: Correct ForeignKey definition
    start_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=255, default='Not Started')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(ProjectUser, on_delete=models.CASCADE)
    role_within_project = models.CharField(max_length=255)

    class Meta:
        unique_together = ('project', 'user') # Ensure no duplicate entries

    def __str__(self):
        return f"{self.user.username} - {self.role_within_project} in {self.project.name}"

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    assignee = models.ForeignKey(ProjectUser, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=255, default='To Do')
    priority = models.CharField(max_length=255, default='Medium')
    notes = models.TextField(blank=True, null=True)
    progress = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserRole(models.Model):
    user = models.ForeignKey(ProjectUser, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

class Notification(models.Model):
    user = models.ForeignKey(ProjectUser, on_delete=models.CASCADE)
    message = models.TextField()
    notification_type = models.CharField(max_length=255)
    related_object_id = models.IntegerField(null=True, blank=True)
    related_object_type = models.CharField(max_length=255, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    delivery_method = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class UserCommunicationChannel(models.Model):
    user = models.ForeignKey(ProjectUser, on_delete=models.CASCADE)
    platform = models.CharField(max_length=255)
    platform_id = models.CharField(max_length=255)

    class Meta:
        unique_together = ('user', 'platform')

    def __str__(self):
        return f"{self.user.username} - {self.platform}: {self.platform_id}"