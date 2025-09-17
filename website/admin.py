from django.contrib import admin
from django.utils.translation import gettext as _
from django.utils.html import format_html
from .models.contact import ContactMessage
from .models.resume import Resume
from .models.schedule import VisitSchedule

# Customize admin site header and title
admin.site.site_header = _("Marcela Vitor Admin")
admin.site.site_title = _("Marcela Vitor Admin")
admin.site.index_title = _("Welcome to Marcela Vitor Learning Center Admin")

# Add custom admin header with link to custom admin panel
admin.site.index_template = 'admin/custom_index.html'

@admin.register(VisitSchedule)
class VisitScheduleAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'visit_date', 'time_slot', 'status', 'admin_panel_link')
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
    
    def admin_panel_link(self, obj):
        return format_html('<a href="/admin-panel/visits/{}" class="button" style="background-color: #1253EF; color: white; padding: 5px 10px; border-radius: 4px; text-decoration: none;">View in Admin Panel</a>', obj.id)
    admin_panel_link.short_description = _("Admin Panel")

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'field_of_expertise', 'admin_panel_link')
    search_fields = ('full_name', 'email', 'phone', 'field_of_expertise')
    list_filter = ('created_at', 'native_language', 'english_level', 'portuguese_level')
    readonly_fields = ('created_at', 'update_at')
    
    def admin_panel_link(self, obj):
        return format_html('<a href="/admin-panel/resumes/{}" class="button" style="background-color: #1253EF; color: white; padding: 5px 10px; border-radius: 4px; text-decoration: none;">View in Admin Panel</a>', obj.id)
    admin_panel_link.short_description = _("Admin Panel")

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = _("Mark selected messages as read")
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = _("Mark selected messages as unread")