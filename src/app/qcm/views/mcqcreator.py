from django.shortcuts import render
from django.views import View
from app.qcm.forms.mcqcreator import MCQCreator
from qa.mcq_models_db import get_questions_db, MCQModel


class MCQModelView(View):
    template_name = 'qcm/mcqcreator.html'

    def get(self, request):
        form = MCQCreator()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form_dict = topics = dict(request.POST.lists())
        del form_dict['csrfmiddlewaretoken']
        form = MCQCreator(request.POST)
        if not form.is_valid():
            print("pas content ! ")
            print(form.cleaned_data)
            return render(request, self.template_name, context={"form": form})
        print(form.cleaned_data)
        question_db = get_questions_db()
        question = MCQModel(
            topics=["Tronc commun"],
            question=form.cleaned_data["question"],
            correct_answers=form.cleaned_data["right_answers"].split("\n"),
            wrong_answers=form.cleaned_data["wrong_answers"].split("\n")
        )
        question_db.add_question(question)
        form = MCQCreator()
        return render(request, self.template_name, context={"form": form})
