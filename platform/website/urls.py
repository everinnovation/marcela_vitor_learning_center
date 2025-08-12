from django.urls import path
from .views.home import HomeView
from .views.about import AboutView
from .views.contact import ContactView
from .views.resume import ResumeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('resume/', ResumeView.as_view(), name='resume'),
]