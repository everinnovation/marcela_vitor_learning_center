from django import forms
from ..models.resume import Resume


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            'full_name', 'email', 'phone', 'city', 'state', 'zip_code',
            'native_language', 'portuguese_level', 'english_level',
            'field_of_expertise', 'years_of_experience', 'resume_file',
            'additional_info'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500'}),
            'city': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500'}),
            'state': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500'}),
            'zip_code': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500'}),
            'native_language': forms.Select(attrs={'class': 'appearance-none w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500 bg-[#f9f9f9]'}),
            'portuguese_level': forms.Select(attrs={'class': 'appearance-none w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500 bg-[#f9f9f9]'}),
            'english_level': forms.Select(attrs={'class': 'appearance-none w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500 bg-[#f9f9f9]'}),
            'field_of_expertise': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500'}),
            'resume_file': forms.FileInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500 text-[#1253EF] file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-[#1253EF] file:text-white hover:file:bg-[#0e49d1] file:cursor-pointer file:transition file:duration-200'}),
            'additional_info': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500', 'rows': 4}),
        }