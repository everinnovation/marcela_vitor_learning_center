from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = 'front/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_start_color'] = 'var(--primary-color)'
        context['navbar_scroll_color'] = 'var(--primary-color)'
        return context
