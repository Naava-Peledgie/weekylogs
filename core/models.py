from django.db import models
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class WeeklyLog(models.Model):

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weekly_logs')

    week_number = models.PositiveIntegerField()
    week_start_date = models.DateField()

    activities = models.TextField()
    challenges = models.TextField(blank=True, null=True)
    skills_gained = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    supervisor_comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'week_number')
        ordering = ['-week_number']

    def __str__(self):
        return f"{self.student} - Week {self.week_number}"
