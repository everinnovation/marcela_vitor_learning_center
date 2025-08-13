from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.utils import timezone
from django.db.models import Count
from ..models.schedule import VisitSchedule
from ..models.resume import Resume
import datetime

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    """Admin dashboard showing summary statistics."""
    template_name = 'admin/dashboard.html'
    login_url = '/admin/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get current date
        today = timezone.now().date()
        
        # Count upcoming visits (from today forward)
        upcoming_visits = VisitSchedule.objects.filter(
            visit_date__gte=today,
            status='scheduled'
        ).count()
        
        # Count completed visits
        completed_visits = VisitSchedule.objects.filter(
            status='completed'
        ).count()
        
        # Count cancelled visits
        cancelled_visits = VisitSchedule.objects.filter(
            status='cancelled'
        ).count()
        
        # Count total visits
        total_visits = VisitSchedule.objects.count()
        
        # Count resume submissions
        total_resumes = Resume.objects.count()
        
        # Get upcoming visits for the next 7 days
        next_week = today + datetime.timedelta(days=7)
        upcoming_week_visits = VisitSchedule.objects.filter(
            visit_date__gte=today,
            visit_date__lte=next_week,
            status='scheduled'
        ).order_by('visit_date', 'time_slot')
        
        # Get recent resume submissions (last 5)
        recent_resumes = Resume.objects.all().order_by('-created_at')[:5]
        
        # Add all data to context
        context.update({
            'upcoming_visits': upcoming_visits,
            'completed_visits': completed_visits,
            'cancelled_visits': cancelled_visits,
            'total_visits': total_visits,
            'total_resumes': total_resumes,
            'upcoming_week_visits': upcoming_week_visits,
            'recent_resumes': recent_resumes,
            'page_title': _('Admin Dashboard')
        })
        
        return context


class VisitListView(LoginRequiredMixin, ListView):
    """View to list all visit schedules."""
    model = VisitSchedule
    template_name = 'admin/visit_list.html'
    context_object_name = 'visits'
    paginate_by = 10
    login_url = '/admin/login/'
    
    def get_queryset(self):
        """Filter visits based on status if provided."""
        queryset = super().get_queryset().order_by('-visit_date', 'time_slot')
        status = self.request.GET.get('status')
        
        if status and status in dict(VisitSchedule.VISIT_STATUS_CHOICES):
            queryset = queryset.filter(status=status)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Visit Schedules')
        context['status_filter'] = self.request.GET.get('status', '')
        return context


class VisitDetailView(LoginRequiredMixin, DetailView):
    """View to show details of a visit schedule."""
    model = VisitSchedule
    template_name = 'admin/visit_detail.html'
    context_object_name = 'visit'
    login_url = '/admin/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Visit Details')
        return context


class ResumeListView(LoginRequiredMixin, ListView):
    """View to list all resume submissions."""
    model = Resume
    template_name = 'admin/resume_list.html'
    context_object_name = 'resumes'
    paginate_by = 10
    login_url = '/admin/login/'
    
    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Resume Submissions')
        return context


class ResumeDetailView(LoginRequiredMixin, DetailView):
    """View to show details of a resume submission."""
    model = Resume
    template_name = 'admin/resume_detail.html'
    context_object_name = 'resume'
    login_url = '/admin/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Resume Details')
        return context
