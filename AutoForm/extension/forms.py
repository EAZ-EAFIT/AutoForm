from django import forms

class pdf_upload(forms.Form):
    pdf_file = forms.FileField(label="Subir archivo PDF")