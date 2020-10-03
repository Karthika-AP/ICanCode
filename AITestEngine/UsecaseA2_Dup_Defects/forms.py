# -*- coding: utf-8 -*-
from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
        )
class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs=
        {'multiple': True, 'webkitdirectory': True, 'directory': True}))