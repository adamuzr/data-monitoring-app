from django import forms
from ..models.alert_model import AlertModel

class AlertForm(forms.ModelForm):
    class Meta:
        model = AlertModel
        fields = ['alert_name', 'rule', 'alert_status']