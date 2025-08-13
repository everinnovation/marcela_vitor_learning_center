from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.views import View
from django.conf import settings


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
                # Continue without the attachment

        try:
            print("Attempting to send email...")
            sent = email.send()
            print(f"Email sent: {sent > 0}")
            return sent > 0
        except Exception as e:
            print(f"Error sending email: {e}")
            return False