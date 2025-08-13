from django.urls import path
from .views.home import HomeView
from .views.about import AboutView
from .views.contact import ContactView
from .views.resume import ResumeView
from .views.schedule import ScheduleView, ScheduleAvailabilityView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('resume/', ResumeView.as_view(), name='resume'),
    path('schedule/', ScheduleView.as_view(), name='schedule'),
    path('check-availability/', ScheduleAvailabilityView.as_view(), name='check_availability'),
]