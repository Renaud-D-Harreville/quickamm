import json
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from qa.mcq_db.models import MCQData  # Assurez-vous que MCQData est bien accessible depuis ce fichier.

from django import forms


class MCQCreatorForm(forms.Form):
    json_input = forms.CharField(
        label="JSON de la question",
        widget=forms.Textarea(attrs={'rows': 20, 'class': 'form-control'}),
        help_text="Entrez le JSON correspondant à un objet MCQData."
    )


class MCQModelViewer(View):
    template_name = 'qcm/mcq-viewer.html'

    def get(self, request):
        """
        Affichage de la page avec un formulaire vide.
        """
        return render(request, self.template_name, context={"json_input": None, "question": None})

    def post(self, request):
        """
        Validation du JSON soumis. Si le JSON est valide, il est transformé en un objet MCQData.
        Sinon, un message d'erreur est affiché.
        """
        json_input = request.POST.get("json_input", "").strip()
        context = {"json_input": json_input, "question": None}

        # Validation et conversion du JSON.
        if json_input:
            try:
                data = json.loads(json_input)
                # Conversion du dictionnaire JSON en un objet MCQData.
                question = MCQData(**data)
                context["question"] = question
                json_question = question.model_dump_json()
                context["json_question"] = json_question
            except (json.JSONDecodeError, TypeError, ValueError) as e:
                context["error"] = f"Erreur de validation du JSON : {str(e)}"

        return render(request, self.template_name, context)
