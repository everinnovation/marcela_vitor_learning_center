from django.views.generic import TemplateView, ListView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
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
        form = ResumeForm(request.POST, request.FILES)

        if form.is_valid():
            resume = form.save()

            # subject = f"Nova mensagem de {contact_message.name} - {contact_message.subject}"
            # context = {
            #     'name': contact_message.name,
            #     'email': contact_message.email,
            #     'number': contact_message.phone,
            #     'subject': contact_message.subject,
            #     'message': contact_message.message
            # }

            # template_name = 'email/contact_email.html'
            # to_emails = ['contatoondecomeremmarica@gmail.com', 'ondecomeremmarica@gmail.com']
            # email_sent = EmailManagementView.send_email(subject, template_name, context, to_emails)

            # if email_sent:
            messages.success(request, 'Thank you for submitting your resume! We will review it and get in touch if there is a match.')
            return redirect('resume')

            # else:
            #     messages.error(request, 'Failed to send email. Please try again.')
            #     return redirect('resume')
        else:
            messages.error(request, 'Please correct the errors below and try again.')
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)
    

class AdminContactMessageListView(ListView):
    model = ContactMessage
    template_name = 'admin/contact_messages_list.html'
    context_object_name = 'contact_messages'
    paginate_by = 10