from django.db import models
from ._base import BaseModel


class VisitSchedule(BaseModel):
    """Model for scheduling daycare visits."""
    
    VISIT_STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    TIME_SLOT_CHOICES = (
        ('09:00', '9:00 AM'),
        ('10:00', '10:00 AM'),
        ('11:00', '11:00 AM'),
        ('14:00', '2:00 PM'),
        ('15:00', '3:00 PM'),
        ('16:00', '4:00 PM'),
    )
    
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    visit_date = models.DateField()
    time_slot = models.CharField(max_length=10, choices=TIME_SLOT_CHOICES)
    number_of_children = models.PositiveSmallIntegerField(default=1)
    children_ages = models.CharField(max_length=100, help_text="Example: 2, 4, 6")
    special_requests = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=VISIT_STATUS_CHOICES, default='scheduled')
    google_calendar_event_id = models.CharField(max_length=1024, blank=True, null=True)
    
    def __str__(self):
        return f"Visit by {self.full_name} on {self.visit_date} at {self.time_slot}"
    
    class Meta:
        verbose_name = "Visit Schedule"
        verbose_name_plural = "Visit Schedules"
        ordering = ['-visit_date', 'time_slot']
