from django import forms
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta
from ..models.schedule import VisitSchedule


class VisitScheduleForm(forms.ModelForm):
    """Form for scheduling a visit to the daycare."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get dates starting from tomorrow for the next 30 days
        tomorrow = date.today() + timedelta(days=1)
        available_dates = [(tomorrow + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]
        
        # Filter weekends (where weekday() returns 5 for Saturday and 6 for Sunday)
        available_dates = [d for d in available_dates if not date.fromisoformat(d).weekday() >= 5]
        
        # Format dates for display
        date_choices = [(d, date.fromisoformat(d).strftime('%d/%m/%Y')) for d in available_dates]
        
        self.fields['visit_date'] = forms.ChoiceField(
            choices=date_choices,
            widget=forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500 bg-[#f9f9f9]'})
        )
    
    class Meta:
        model = VisitSchedule
        fields = [
            'full_name', 'email', 'phone', 'visit_date', 'time_slot', 
            'number_of_children', 'children_ages', 'special_requests'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500'}),
            'time_slot': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500 bg-[#f9f9f9]'}),
            'number_of_children': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500', 'min': '1', 'max': '5'}),
            'children_ages': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500', 'placeholder': _('Example: 2, 4, 6')}),
            'special_requests': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500', 'rows': 4}),
        }
