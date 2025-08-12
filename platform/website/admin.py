from django.contrib import admin
from .models.contact import ContactMessage
from .models.resume import Resume

admin.site.register(ContactMessage)
admin.site.register(Resume)