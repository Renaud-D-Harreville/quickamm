from django.shortcuts import render
from django.views import View
from qa.mcq_factories import AllQuestionsFactory
from qa.mcq import MultipleChoiceQuestion
from app.qcm.forms import QCMForm, TopicForm
from app.qcm.requests_facades import IndexPostRequestFacade

all_questions_factory: AllQuestionsFactory = AllQuestionsFactory()


class QuestionView(View):
    template_name = 'qcm/question/index.html'

    @staticmethod
    def _get_form_from_question(question: MultipleChoiceQuestion) -> QCMForm:
        form = QCMForm()
        form.fields['question'].initial = question.dict()
        form.fields['text_answers'].choices = [(index, answer) for index, answer in
                                               enumerate(question.answers)]
        return form

    @staticmethod
    def _get_topic_form(initial: str = "AMM") -> TopicForm:
        form = TopicForm()
        form.fields['topic_list'].choices = [(topic, topic) for topic in all_questions_factory.topics]
        form.fields["topic_list"].initial = initial
        return form

    def get(self, request):
        topics = dict(request.GET.lists())["topic_list"] if "topic_list" in request.GET else ["AMM"]
        question = all_questions_factory.get_random_question_from_topics(topics)
        form = self._get_form_from_question(question)
        json_question = question.to_mcq_data().model_dump_json()
        context_dict = {
            "question": question,
            "json_question": json_question,
            "form": form,
            "topic_form": self._get_topic_form(topics),
            "topic_list": topics
        }
        return render(request, self.template_name, context_dict)

    def post(self, request):
        topics = dict(request.POST.lists())["topic_list"] if "topic_list" in request.POST else ["AMM"]
        req_facade = IndexPostRequestFacade(request)
        question = req_facade.mcq

        context_dict = {
            "question": question,
            'form': self._get_form_from_question(question),
            "topic_form": self._get_topic_form(),
            'small_response': req_facade.get_small_response(),
            "complete_response": [1 + index for index in question.correct_indexes],
            "explanation": question.answer_description,
            # "correction_link": question.correction_link
            "topic_list": topics
        }
        return render(request, self.template_name, context_dict)