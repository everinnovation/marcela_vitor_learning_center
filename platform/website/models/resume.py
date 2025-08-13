from django.db import models
from ._base import BaseModel
from django.core.validators import FileExtensionValidator


class Resume(BaseModel):
    LANGUAGE_CHOICES = [
        ('portuguese', 'Portuguese'),
        ('english', 'English'),
        ('other', 'Other'),
    ]

    LANGUAGE_LEVEL_CHOICES = [
        ('native', 'Native'),
        ('fluent', 'Fluent'),
        ('intermediate', 'Intermediate'),
        ('basic', 'Basic'),
    ]

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    native_language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES)
    portuguese_level = models.CharField(max_length=20, choices=LANGUAGE_LEVEL_CHOICES)
    english_level = models.CharField(max_length=20, choices=LANGUAGE_LEVEL_CHOICES)
    field_of_expertise = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    resume_file = models.FileField(upload_to='curriculos/', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])])
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name