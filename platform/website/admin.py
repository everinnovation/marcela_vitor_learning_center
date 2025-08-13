from django.contrib import admin
from .models.contact import ContactMessage
from .models.resume import Resume
from .models.schedule import VisitSchedule

@admin.register(VisitSchedule)
class VisitScheduleAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'visit_date', 'time_slot', 'status')
    list_filter = ('status', 'visit_date')
    search_fields = ('full_name', 'email', 'phone')
    readonly_fields = ('created_at', 'update_at', 'google_calendar_event_id')
    fieldsets = (
        (None, {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Visit Details', {
            'fields': ('visit_date', 'time_slot', 'number_of_children', 'children_ages', 'special_requests')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('System Information', {
            'fields': ('created_at', 'update_at', 'google_calendar_event_id'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(ContactMessage)
admin.site.register(Resume)