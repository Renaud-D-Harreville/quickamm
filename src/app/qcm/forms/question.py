from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.safestring import mark_safe


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


class TopicCheckboxSelectMultiple(CheckboxSelectMultiple):

    def get_space_label(self, label: str) -> str:
        split_label = label.split("/")
        nb_space = (len(split_label) -1) * 1
        spaces = "> " * nb_space
        space_label = f"{spaces}{split_label[-1]}"
        return space_label

    def render(self, name, value, attrs=None, renderer=None):
        output = []
        for i, (option_value, option_label) in enumerate(self.choices):
            space_label = self.get_space_label(option_label)
            input_id = f"{name}_{i}"
            field_str = f"""
            <div class="topic-button">
                <input type="radio" name="{name}" value="{option_value}" id="{input_id}"> 
                <label for="{input_id}">{space_label}</label>
            </div>
            """
            output.append(field_str)
        return mark_safe('\n'.join(output))


class QCMForm(forms.Form):
    question = forms.JSONField(widget=forms.HiddenInput)
    text_answers = forms.MultipleChoiceField(widget=MCQCheckboxSelectMultiple, label="")


class TopicForm(forms.Form):
    topic_list = forms.MultipleChoiceField(widget=TopicCheckboxSelectMultiple, label="")
