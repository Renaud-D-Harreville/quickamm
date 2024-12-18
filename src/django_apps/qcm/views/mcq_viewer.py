import json
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from qa.mcq_db.models import MCQData

from django import forms


class MCQCreatorForm(forms.Form):
    json_input = forms.JSONField()


class MCQModelViewer(View):
    template_name = 'qcm/mcq-viewer.html'

    def get(self, request):
        form = MCQCreatorForm()  # Initialisation d'un formulaire vide
        context = {"form": form, "json_input": None, "question": None}
        return render(request, self.template_name, context=context)

    def post(self, request):
        """
        Validation du JSON soumis via le formulaire MCQCreatorForm.
        Affiche les erreurs de validation si le JSON est invalide.
        """
        form = MCQCreatorForm(request.POST)
        context = {"form": form, "question": None}

        if form.is_valid():
            try:
                data = form.cleaned_data["json_input"]
                # Conversion du dictionnaire JSON en un objet MCQData.
                question = MCQData(**data)
                context["question"] = question
                json_question = question.model_dump_json()
                context["json_question"] = json_question
            except (TypeError, ValueError) as e:
                form.add_error("json_input", f"Erreur de validation des données : {str(e)}")

        return render(request, self.template_name, context)
