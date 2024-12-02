from django.shortcuts import render
from django.views import View
from qa.mcq_models_db import get_questions_db


class MCQModelView(View):
    template_name = 'qcm/mcqmodelviewer.html'

    def get(self, request):
        questiondb = get_questions_db()
        return render(request, self.template_name, context={"questions": questiondb})
