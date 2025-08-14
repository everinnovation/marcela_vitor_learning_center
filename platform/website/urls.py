from django.urls import path
from .views.home import HomeView
from .views.about import AboutView
from .views.contact import ContactView
from .views.resume import ResumeView
from .views.schedule import ScheduleView, ScheduleAvailabilityView
from .views.programs import ProgramsView
from .views.admin_panel import (
    AdminDashboardView, VisitListView, VisitDetailView,
    ResumeListView, ResumeDetailView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('resume/', ResumeView.as_view(), name='resume'),
    path('schedule/', ScheduleView.as_view(), name='schedule'),
    path('programs/', ProgramsView.as_view(), name='programs'),
    path('check-availability/', ScheduleAvailabilityView.as_view(), name='check_availability'),
    
    # Admin panel URLs
    path('admin-panel/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin-panel/visits/', VisitListView.as_view(), name='admin_visits'),
    path('admin-panel/visits/<int:pk>/', VisitDetailView.as_view(), name='admin_visit_detail'),
    path('admin-panel/resumes/', ResumeListView.as_view(), name='admin_resumes'),
    path('admin-panel/resumes/<int:pk>/', ResumeDetailView.as_view(), name='admin_resume_detail'),
]