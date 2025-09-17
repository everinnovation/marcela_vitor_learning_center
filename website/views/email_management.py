from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.views import View
from django.conf import settings
import logging
import os

logger = logging.getLogger(__name__)

class EmailManagementView(View):
    def send_email(subject, template_name, context, to_emails, file_path=None, file_name=None):
        print(f"Sending email with subject: {subject}")
        print(f"To: {to_emails}")
        
        message = render_to_string(template_name, context)
        from_email = settings.EMAIL_FROM
        email = EmailMessage(subject, message, from_email, to=to_emails)
        email.content_subtype = 'html'

        if file_path:
            print(f"Attaching file: {file_path}")
            try:
                with open(file_path, 'rb') as pdf_file:
                    file_extension = file_path.split('.')[-1]
                    content_type = 'application/pdf' if file_extension == 'pdf' else 'application/octet-stream'
                    if file_extension in ['doc', 'docx']:
                        content_type = 'application/msword'
                    email.attach(f'{file_name}.{file_extension}', pdf_file.read(), content_type)
                    print(f"File attached successfully: {file_name}.{file_extension}")
            except Exception as e:
                print(f"Error attaching file: {e}")

        try:
            print("Attempting to send email...")
            sent = email.send()
            print(f"Email sent: {sent > 0}")
            return sent > 0
        except Exception as e:
            print(f"Error sending email: {e}")
            return False


class EmailManager:
    @staticmethod
    def send_resume_email(resume_data, file_path=None):
        """Send email notification for new resume submission."""
        try:
            email_html = render_to_string('email/resume_email.html', {
                'name': resume_data.full_name,
                'email': resume_data.email,
                'phone': resume_data.phone,
                'city': resume_data.city,
                'state': resume_data.state,
                'zip_code': resume_data.zip_code,
                'native_language': resume_data.get_native_language_display(),
                'portuguese_level': resume_data.get_portuguese_level_display(),
                'english_level': resume_data.get_english_level_display(),
                'field_of_expertise': resume_data.field_of_expertise,
                'years_of_experience': resume_data.years_of_experience,
                'additional_info': resume_data.additional_info
            })
            
            email = EmailMessage(
                subject=f'New Resume Submission - {resume_data.full_name}',
                body=email_html,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.ADMIN_EMAIL],
                reply_to=[resume_data.email]
            )
            email.content_subtype = "html"
            
            if file_path and os.path.exists(file_path):
                file_name = os.path.basename(file_path)
                file_extension = file_name.split('.')[-1]
                
                content_type = 'application/pdf' if file_extension.lower() == 'pdf' else 'application/octet-stream'
                
                with open(file_path, 'rb') as pdf_file:
                    email.attach(f'{file_name}', pdf_file.read(), content_type)
                    
                logger.info(f"Resume file attached: {file_name}")
            else:
                logger.warning(f"Resume file not found or not provided: {file_path}")
            
            email.send()
            logger.info(f"Resume notification email sent for {resume_data.full_name}")
            return True
        
        except Exception as e:
            logger.error(f"Error sending resume email: {str(e)}")
            return False
            
    @staticmethod
    def send_schedule_confirmation_email(schedule_data):
        try:
            hour = int(schedule_data.time_slot.split(':')[0])
            minute = schedule_data.time_slot.split(':')[1]
            ampm = 'PM' if hour >= 12 else 'AM'
            formatted_hour = hour % 12 or 12
            formatted_time = f"{formatted_hour}:{minute} {ampm}"
            
            formatted_date = schedule_data.visit_date.strftime('%A, %B %d, %Y')
            
            email_html = render_to_string('email/schedule_email.html', {
                'name': schedule_data.full_name,
                'email': schedule_data.email,
                'visit_date': formatted_date,
                'time_slot': formatted_time,
                'number_of_children': schedule_data.number_of_children,
                'children_ages': schedule_data.children_ages,
                'special_requests': schedule_data.special_requests
            })
            
            admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
            contact_email = "contactmarcelavitor@gmail.com"
            
            customer_email = EmailMessage(
                subject=f'Visit Confirmation - Marcela Vitor Learning Center',
                body=email_html,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[schedule_data.email],
                reply_to=[contact_email]
            )
            customer_email.content_subtype = "html"
            customer_email.send()
            
            admin_email_msg = EmailMessage(
                subject=f'New Visit Scheduled - {schedule_data.full_name}',
                body=email_html,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[admin_email],
                reply_to=[schedule_data.email]
            )
            admin_email_msg.content_subtype = "html"
            admin_email_msg.send()
            
            contact_email_msg = EmailMessage(
                subject=f'New Visit Scheduled - {schedule_data.full_name}',
                body=email_html,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[contact_email],
                reply_to=[schedule_data.email]
            )
            contact_email_msg.content_subtype = "html"
            contact_email_msg.send()
            
            logger.info(f"Schedule confirmation emails sent for {schedule_data.full_name} to customer, admin, and contact")
            return True
        
        except Exception as e:
            logger.error(f"Error sending schedule confirmation email: {str(e)}")
            return False