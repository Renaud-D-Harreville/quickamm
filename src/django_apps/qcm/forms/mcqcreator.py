from django import forms


class MCQCreator(forms.Form):

    question: forms.CharField = forms.CharField(label="Question", help_text="Mettre la question du QCM")
    right_answers: forms.CharField = forms.CharField(label="Réponses vraies possibles", widget=forms.Textarea)
    wrong_answers: forms.CharField = forms.CharField(label="Réponses fausses possibles", widget=forms.Textarea)

    def get_right_answers(self) -> list[str]:
        return self.cleaned_data['right_answers'].split('\n')

    def get_wrong_answers(self) -> list[str]:
        return self.cleaned_data['wrong_answers'].split('\n')
