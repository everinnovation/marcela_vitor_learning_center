from django.views.generic import TemplateView
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

class CalendarView(TemplateView):
    """View for displaying the embedded Google Calendar."""
    template_name = 'front/calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add calendar URLs to the context
        context['calendar_embed_url'] = 'https://calendar.google.com/calendar/embed?src=contactmarcelavitor%40gmail.com&ctz=America%2FSao_Paulo'
        context['calendar_ical_url'] = 'https://calendar.google.com/calendar/ical/contactmarcelavitor%40gmail.com/public/basic.ics'
        
        return context
    
def calendar_embed(request):
    """Simple view that returns the calendar embed HTML."""
    calendar_embed_html = """
    <iframe src="https://calendar.google.com/calendar/embed?src=contactmarcelavitor%40gmail.com&ctz=America%2FSao_Paulo" 
            style="border: 0" 
            width="800" 
            height="600" 
            frameborder="0" 
            scrolling="no">
    </iframe>
    """
    return HttpResponse(calendar_embed_html)
