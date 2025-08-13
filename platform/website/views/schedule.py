import json
import logging
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from ..forms.schedule import VisitScheduleForm
from ..models.schedule import VisitSchedule
from ..utils.google_calendar import GoogleCalendarService
from .email_management import EmailManager

logger = logging.getLogger(__name__)

class ScheduleView(TemplateView):
    """View for scheduling daycare visits."""
    template_name = 'front/schedule.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VisitScheduleForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = VisitScheduleForm(request.POST)
        
        if form.is_valid():
            try:
                # Create the schedule object but don't save yet
                schedule = form.save(commit=False)
                logger.info(f"Processing schedule form for {schedule.full_name} on {schedule.visit_date} at {schedule.time_slot}")
                
                # Initialize the Google Calendar service
                calendar_service = GoogleCalendarService()
                
                # Flag to track if calendar integration was successful
                calendar_success = False
                
                # Try to create a Google Calendar event
                try:
                    logger.info("Attempting to create Google Calendar event")
                    
                    # Execute test to verify calendar service is working
                    if not calendar_service.initialized:
                        logger.warning("Calendar service not properly initialized, attempting to force initialize")
                        # Try initializing with test event
                        if calendar_service.verify_calendar_access():
                            calendar_service.initialized = True
                            logger.info("Successfully initialized calendar service through verification")
                    
                    if calendar_service.initialized:
                        # Log details for debugging
                        logger.info(f"Calendar ID being used: {calendar_service.calendar_id}")
                        logger.info(f"Creating event for {schedule.full_name} on {schedule.visit_date} at {schedule.time_slot}")
                        
                        event_id = calendar_service.create_event(schedule)
                        
                        if event_id:
                            # Save the Google Calendar event ID with the schedule
                            schedule.google_calendar_event_id = event_id
                            calendar_success = True
                            logger.info(f"Calendar event created with ID: {event_id}")
                        else:
                            logger.warning("Google Calendar event creation returned None")
                    else:
                        logger.error("Google Calendar service is not properly initialized")
                except Exception as e:
                    logger.error(f"Exception during Google Calendar event creation: {str(e)}")
                    # Continue without Google Calendar integration
                
                # Save the schedule record even if calendar integration fails
                schedule.save()
                logger.info(f"Schedule saved to database with ID: {schedule.id}")
                
                # Send confirmation emails
                try:
                    logger.info("Sending confirmation email")
                    
                    # Format time slot for better display
                    hour = int(schedule.time_slot.split(':')[0])
                    minute = schedule.time_slot.split(':')[1]
                    ampm = 'PM' if hour >= 12 else 'AM'
                    formatted_hour = hour % 12 or 12
                    formatted_time = f"{formatted_hour}:{minute} {ampm}"
                    
                    # Format date for better display
                    formatted_date = schedule.visit_date.strftime('%A, %B %d, %Y')
                    
                    # Prepare the context for the email template
                    email_context = {
                        'name': schedule.full_name,
                        'email': schedule.email,
                        'phone': schedule.phone,
                        'visit_date': formatted_date,
                        'time_slot': formatted_time,
                        'number_of_children': schedule.number_of_children,
                        'children_ages': schedule.children_ages,
                        'special_requests': schedule.special_requests or 'None'
                    }
                    
                    # Call the EmailManager to send the email
                    email_sent = EmailManager.send_schedule_confirmation_email(schedule)
                    
                    if email_sent:
                        logger.info(f"Confirmation email sent for {schedule.full_name}'s visit")
                    else:
                        logger.warning(f"Failed to send confirmation email for {schedule.full_name}'s visit")
                except Exception as e:
                    logger.error(f"Error sending confirmation email: {str(e)}")
                    email_sent = False
                    # Continue even if email fails
                
                # Show appropriate message based on calendar integration and email success
                if calendar_success and email_sent:
                    messages.success(request, _("Your visit has been scheduled successfully! We've sent a confirmation email with all the details. We'll see you soon."))
                elif calendar_success and not email_sent:
                    messages.success(request, _("Your visit has been scheduled successfully! There was an issue sending the confirmation email, but we'll see you soon."))
                elif not calendar_success and email_sent:
                    messages.warning(
                        request, 
                        _("Your visit has been scheduled and we've sent you a confirmation email. However, there was an issue with the calendar integration. "
                          "Our team will contact you to confirm the appointment.")
                    )
                else:
                    messages.warning(
                        request, 
                        _("Your visit has been scheduled, but there were issues with both the calendar integration and sending the confirmation email. "
                          "Our team will contact you to confirm the appointment.")
                    )
                return redirect('schedule')
            
            except Exception as e:
                logger.error(f"Error scheduling visit: {str(e)}")
                messages.error(request, _("There was an error scheduling your visit. Please try again or contact us directly."))
        else:
            logger.warning(f"Form validation errors: {form.errors}")
            messages.error(request, _("Please correct the errors in the form."))
        
        # If we get here, there was an error
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

@method_decorator(csrf_exempt, name='dispatch')
class ScheduleAvailabilityView(TemplateView):
    """View for checking availability of time slots."""
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            selected_date = data.get('date')
            
            if not selected_date:
                return JsonResponse({'error': 'Date is required'}, status=400)
            
            calendar_service = GoogleCalendarService()
            
            # Check if the service is properly initialized
            if not calendar_service.initialized:
                logger.warning("Google Calendar service is not properly initialized - returning all slots as available")
                all_slots = ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00']
                return JsonResponse({'available_slots': all_slots})
                
            available_slots = calendar_service.get_available_slots(selected_date)
            
            return JsonResponse({
                'available_slots': available_slots
            })
        
        except Exception as e:
            logger.error(f"Error getting available slots: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
