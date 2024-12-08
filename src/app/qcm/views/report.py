from django.shortcuts import render
from django.views import View
from qa.mcq_db.models import MCQData
from qa.mcq_handler.reports import DictOfQuestionReports, get_dict_problems, QuestionReport, QuestionReports
from app.qcm.forms import ReportForm
import json

all_reports: DictOfQuestionReports = get_dict_problems()


class ReportView(View):
    template_name = 'qcm/report.html'

    @staticmethod
    def mcq(data) -> MCQData:
        question_dict = json.loads(data["question"])
        question = MCQData(**question_dict)
        return question

    @staticmethod
    def _get_form(mcq_reports: QuestionReports, mcq: MCQData) -> ReportForm:
        form = ReportForm()
        form.fields['mcq_reports'].initial = mcq_reports.model_dump() if mcq_reports else None
        form.fields['question'].initial = mcq.model_dump()
        form.fields['report'].initial = ""
        return form

    def get(self, request):
        mcq = self.mcq(request.GET)
        mcq_reports = all_reports.get_reports_from_mcq(mcq)
        context_dict = {
            "reports": mcq_reports,
            "mcq_db": mcq,
            "form": self._get_form(mcq_reports, mcq),
            "json_dump": mcq.model_dump_json()
        }
        return render(request, self.template_name, context=context_dict)

    @staticmethod
    def _handle_report(request, mcq: MCQData):
        report = request.POST["report"]
        if report is None:
            return
        question_report = QuestionReport(
            mcq_context=mcq,
            report=report
        )
        all_reports.add_report(question_report)

    def post(self, request):
        mcq = self.mcq(request.POST)
        self._handle_report(request, mcq)
        mcq_reports = all_reports.get_reports_from_mcq(mcq)
        context_dict = {
            "reports": mcq_reports,
            "mcq_db": mcq,
            "form": self._get_form(mcq_reports, mcq)
        }
        return render(request, self.template_name, context=context_dict)
