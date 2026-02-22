from django.db import models

from django.conf import settings
from django.db.models import UniqueConstraint
from django.db.models.functions import TruncDate
from django.core.validators import MinValueValidator, MaxValueValidator

# Service model to represent the service in the system
class Service(models.Model):

    Service_id = models.AutoField(primary_key=True)

    Service_name = models.CharField(max_length=100)

    avg_service_time = models.PositiveBigIntegerField(
                        help_text="Average service time in seconds")
    
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Service_name
    
    class Meta:
        db_table = 'services'

# counter model to reprsent the counter in the system
class Counter(models.Model):
    Counter_id = models.AutoField(primary_key=True)

    Counter_name = models.CharField(max_length=100)

    service = models.ForeignKey('Service', 
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='counters')
    
    is_active = models.BooleanField(default=True)

    staff_name = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Counter_name
    
    class Meta:
        db_table = 'counters'


# Token model to represent the token in the system
class Token(models.Model):

    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('called', 'Called'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    token_id = models.AutoField(primary_key=True)

    token_number = models.CharField(max_length=20)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tokens'
    )

    service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        related_name='tokens'
    )

    counter = models.ForeignKey(
        'Counter',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tokens'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='waiting'
    )

    priority_flag = models.BooleanField(default=False)

    appointment_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    called_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    predicted_wait_time = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Predicted wait time in minutes"
    )

    actual_wait_time = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Actual wait time in minutes"
    )

    notification_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.token_number} - {self.service.service_name}"

    class Meta:
        db_table = "tokens"

        constraints = [
            UniqueConstraint(
                TruncDate('created_at'),
                'service',
                'token_number',
                name='unique_token_per_service_per_day'
            )
        ]
        
    
        indexes = [
        models.Index(fields=['user']),
        models.Index(fields=['service']),
        models.Index(fields=['status']),
        models.Index(fields=['created_at']),
        ]

        



# QueueLog model to represent the queue log in the system

class QueueLog(models.Model):

    log_id = models.AutoField(primary_key=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        related_name='queue_logs'
    )

    queue_length = models.PositiveIntegerField()

    active_counters = models.PositiveIntegerField()

    waiting_count = models.PositiveIntegerField()

    completed_count = models.PositiveIntegerField()

    avg_service_time = models.FloatField()

    max_wait_time = models.PositiveIntegerField()

    min_wait_time = models.PositiveIntegerField()

    peak_hour = models.BooleanField(default=False)

    # 🔹 For ML training
    predicted_wait_time = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    actual_avg_wait_time = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.service.service_name} - {self.timestamp}"

    class Meta:
        db_table = "queue_logs"
        indexes = [
        models.Index(fields=['timestamp']),
    ]





# Notification model to represent the notifications in the system
class Notification(models.Model):

    TYPE_CHOICES = [
        ('token_generated', 'Token Generated'),
        ('turn_approaching', 'Turn Approaching'),
        ('final_call', 'Final Call'),
        ('delay_alert', 'Delay Alert'),
        ('counter_changed', 'Counter Changed'),
    ]

    DELIVERY_STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]

    notification_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    token = models.ForeignKey(
        'Token',
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True
    )

    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES
    )

    message = models.TextField()

    sent_at = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    delivery_status = models.CharField(
        max_length=20,
        choices=DELIVERY_STATUS_CHOICES,
        default='sent'
    )

    def __str__(self):
        return f"{self.user.username} - {self.type}"

    class Meta:
        db_table = "notifications"
        indexes = [
        models.Index(fields=['user', 'is_read']),
    ]





# Feedback model to represent the feedback in the system
class Feedback(models.Model):

    feedback_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='feedbacks'
    )

    token = models.ForeignKey(
        'Token',
        on_delete=models.SET_NULL,
        null=True,
        related_name='feedbacks'
    )

    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Overall service rating (1-5)"
    )

    comments = models.TextField(blank=True, null=True)

    waiting_satisfaction = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Waiting time satisfaction (1-5)"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user} - Rating {self.rating}"

    class Meta:
        db_table = "feedback"
