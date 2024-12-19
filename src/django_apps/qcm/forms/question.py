from django import forms
from django.forms.widgets import CheckboxSelectMultiple


class MCQCheckboxSelectMultiple(CheckboxSelectMultiple):

    def render(self, name, value, attrs=None, renderer=None):
        output = []
        for i, (option_value, option_label) in enumerate(self.choices):
            input_id = f"{name}_{i}"
            field_str = f"""
            <div class="mcq-button">
                <input type="checkbox" name="{name}" value="{option_value}" id="{input_id}"> 
                <label for="{input_id}">{option_label}</label>
            </div>
            """
            output.append(field_str)
        return mark_safe('\n'.join(output))


class QCMForm(forms.Form):
    question = forms.JSONField(widget=forms.HiddenInput)
    text_answers = forms.MultipleChoiceField(widget=MCQCheckboxSelectMultiple, label="")



