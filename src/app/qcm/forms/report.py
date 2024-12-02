from django import forms


class ReportForm(forms.Form):
    mcq_reports = forms.JSONField(widget=forms.HiddenInput)
    question = forms.JSONField(widget=forms.HiddenInput)
    report = forms.CharField(min_length=5, max_length=300, label="Décrivez votre souci", widget=forms.Textarea)
