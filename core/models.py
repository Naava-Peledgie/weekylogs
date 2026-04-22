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
    
    from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

def clean(self):
        # 1. Define the Deadline 7 days 
       submission_deadline = self.week_start_date + timedelta(days=7)

       # 2. Enforce the Deadline 
       if self.status == 'submitted' and timezone.now().date() > submission_deadline:
        raise ValidationError(f"The submission deadline for Week {self.week_number} has passed.")

    # 3. Prevent Future Submissions 
       if self.status == 'submitted' and self.week_start_date > timezone.now().date():
        raise ValidationError("You cannot submit a log for a week that hasn't started yet.")
    
def save(self, *args, **kwargs):
        """
        Handles Week 6 State Transitions and Locking[cite: 15, 142].
        """
        if self.pk:  # If updating an existing record
            original = WeeklyLog.objects.get(pk=self.pk)
            
            # Lock editing: Prevent modifications if the log is already approved 
            if original.status == 'approved':
                raise ValidationError("This log has been approved and can no longer be edited.")

        # Run the clean() method validation before saving to the database
        self.full_clean()
        super().save(*args, **kwargs)