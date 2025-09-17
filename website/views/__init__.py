# Import all views here for easy importing
from .admin_panel import (
    AdminDashboardView, VisitListView, VisitDetailView,
    ResumeListView, ResumeDetailView
)
from .home import HomeView
from .about import AboutView
from .contact import ContactView
from .resume import ResumeView
from .schedule import ScheduleView, ScheduleAvailabilityView

__all__ = [
    'AdminDashboardView',
    'VisitListView',
    'VisitDetailView',
    'ResumeListView',
    'ResumeDetailView',
    'HomeView',
    'AboutView',
    'ContactView',
    'ResumeView',
    'ScheduleView',
    'ScheduleAvailabilityView',
]
