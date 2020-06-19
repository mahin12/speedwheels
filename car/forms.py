from django import forms
from django.core.exceptions import ValidationError

from .models import *


class ReserveForm(forms.ModelForm):
    class Meta:
        model = Reservation
        exclude = ("user", "product", "is_reserved", "cost")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rent_from"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]
        self.fields["rent_to"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

    def clean_rent_to(self):
        if self.cleaned_data['rent_from'] > self.cleaned_data['rent_to']:
            raise ValidationError("From date can not be greater than to date")
        return self.cleaned_data['rent_to']


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        exclude = ("status", "user")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["report_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]
        self.fields["incident_time"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]
