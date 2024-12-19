from django.shortcuts import render
from django.views import View
from django_apps.qcm.forms import QCMForm, TopicForm
from django_apps.qcm.requests_facades import IndexPostRequestFacade
from qa.mcq_db.models import MCQData
from qa.api import api
import abc


class AbstractQuestionView(View, abc.ABC):
    template_name = 'qcm/question/index.html'

    @abc.abstractmethod
    def get_default_topic(self) -> str:
        pass

    @abc.abstractmethod
    def get_topic_list(self) -> list[str]:
        pass

    def get_seed(self) -> str | int | float | None:
        return None

    @staticmethod
    def _get_form_from_question(question: MCQData) -> QCMForm:
        form = QCMForm()
        form.fields['question'].initial = question.model_dump()
        form.fields['text_answers'].choices = [(index, answer) for index, answer in
                                               enumerate(question.answers)]
        return form

    def _get_topic_form(self, initial: str = "AMM") -> TopicForm:
        form = TopicForm()
        form.fields['topic_list'].choices = [(topic, topic) for topic in self.get_topic_list()]
        form.fields["topic_list"].initial = initial
        return form

    def get(self, request):
        topics = dict(request.GET.lists())["topic_list"] \
            if "topic_list" in request.GET else [self.get_default_topic()]
        seed = self.get_seed()
        question = api.get_random_question_from_topics(topics, seed)
        form = self._get_form_from_question(question)
        json_question = question.model_dump_json()
        context_dict = {
            "question": question,
            "json_question": json_question,
            "form": form,
            "topic_form": self._get_topic_form(topics),
            "topic_list": topics
        }
        return render(request, self.template_name, context_dict)

    # def post(self, request):
    #     topics = dict(request.POST.lists())["topic_list"] \
    #         if "topic_list" in request.POST else [self.get_default_topic()]
    #     req_facade = IndexPostRequestFacade(request)
    #     question = req_facade.mcq
    #
    #     context_dict = {
    #         "question": question,
    #         'form': self._get_form_from_question(question),
    #         "topic_form": self._get_topic_form(),
    #         'small_response': req_facade.get_small_response(),
    #         "complete_response": [1 + index for index in question.correct_indexes],
    #         "explanation": question.answer_description,
    #         # "correction_link": question.correction_link
    #         "topic_list": topics
    #     }
    #     return render(request, self.template_name, context_dict)




