from django.views.generic import TemplateView, ListView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.utils.translation import gettext as _
from ..forms.resume import ResumeForm
from ..models.contact import ContactMessage
from ..views.email_management import EmailManagementView


class ResumeView(TemplateView):
    template_name = 'front/resume.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_email'] = ''
        context['form'] = ResumeForm()
        return context
    
    def post(self, request, *args, **kwargs):
        print("Resume form submitted")
        print(f"POST data: {request.POST}")
        print(f"FILES data: {request.FILES}")
        
        form = ResumeForm(request.POST, request.FILES)

        if form.is_valid():
            print("Form is valid")
            try:
                resume = form.save()
                print(f"Resume saved successfully with ID: {resume.id}")
            except Exception as e:
                print(f"Error saving resume: {e}")
                messages.error(request, _('There was an error saving your resume. Please try again.'))
                context = self.get_context_data(**kwargs)
                context['form'] = form
                return self.render_to_response(context)

            subject = _('New resume submitted by {}').format(resume.full_name)
            context = {
                'name': resume.full_name,
                'email': resume.email,
                'phone': resume.phone,
                'city': resume.city,
                'state': resume.state,
                'zip_code': resume.zip_code,
                'native_language': resume.get_native_language_display(),
                'portuguese_level': resume.get_portuguese_level_display(),
                'english_level': resume.get_english_level_display(),
                'field_of_expertise': resume.field_of_expertise,
                'years_of_experience': resume.years_of_experience,
                'additional_info': resume.additional_info,
                'resume_file_url': request.build_absolute_uri(resume.resume_file.url) if resume.resume_file else 'No file submitted'
            }

            template_name = 'email/resume_email.html'
            to_emails = [getattr(settings, 'ADMIN_EMAIL', 'marcelavitorlearningcenter@gmail.com')]
            
            try:
                if resume.resume_file:
                    try:
                        file_path = resume.resume_file.path
                        safe_name = ''.join(c for c in resume.full_name if c.isalnum() or c.isspace()).strip().replace(' ', '_')
                        file_name = f"Resume_{safe_name}"
                        email_sent = EmailManagementView.send_email(subject, template_name, context, to_emails, file_path, file_name)
                    except Exception as e:
                        print(f"Error accessing resume file: {e}")
                        email_sent = EmailManagementView.send_email(subject, template_name, context, to_emails)
                else:
                    email_sent = EmailManagementView.send_email(subject, template_name, context, to_emails)
            except Exception as e:
                print(f"Error sending email: {e}")
                email_sent = False

            if email_sent:
                messages.success(request, _('Thank you for submitting your resume! We will review it and get in touch if there is a match.'))
                return redirect('resume')
            else:
                messages.error(request, _('Your resume was saved, but we couldn\'t send the notification email. We\'ll still review your application.'))
                return redirect('resume')
        else:
            print("Form is not valid")
            print(f"Form errors: {form.errors}")
            messages.error(request, _('Please correct the errors below and try again.'))
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
    

class AdminContactMessageListView(ListView):
    model = ContactMessage
    template_name = 'admin/contact_messages_list.html'
    context_object_name = 'contact_messages'
    paginate_by = 10