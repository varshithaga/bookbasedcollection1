from django import forms
from .models import UploadedFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']  # or your file field name

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not (file.name.endswith('.pdf') or file.name.endswith('.txt') or file.name.endswith('.docx')):
                raise forms.ValidationError("Only PDF, TXT, or DOCX files are allowed.")
        return file
