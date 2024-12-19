from django.shortcuts import render
from django.views import View
from django_apps.qcm.forms import QCMForm, TopicForm
from qa.mcq_db.models import MCQData
from qa.api import api

from qa.topics.themes import Theme


class ThemeQuestionView(View):
    template_name = 'qcm/question/index.html'
    DEFAULT_THEME = api.get_theme_from_path(["Probatoire AMM"])

    def _get_current_theme(self, request):
        if 'current_theme' not in request.session:
            current_theme = self.DEFAULT_THEME
            request.session['current_theme'] = current_theme.model_dump()
            request.session.modified = True  # Indiquer que la session a été modifiée

        dict_theme = request.session['current_theme']
        theme = Theme(**dict_theme)
        return theme

    def get_seed(self) -> str | int | float | None:
        return None

    @staticmethod
    def _get_form_from_question(question: MCQData) -> QCMForm:
        form = QCMForm()
        form.fields['question'].initial = question.model_dump()
        form.fields['text_answers'].choices = [(index, answer) for index, answer in
                                               enumerate(question.answers)]
        return form

    def _get_choices_from_theme(self, theme: Theme) -> list[tuple[str, str]]:
        main_theme_choice = (theme.identifier, theme.name)
        sub_themes_choices = [(sub_theme.identifier, f" > {sub_theme.name}") for _, sub_theme in theme.sub_themes.items()]
        return [main_theme_choice] + sub_themes_choices

    def _get_topic_form(self, theme: Theme, initial: str = None) -> TopicForm:
        if initial is None:
            initial = theme.identifier
        form = TopicForm()
        form.fields['topic_list'].choices = self._get_choices_from_theme(theme)
        form.fields["topic_list"].initial = initial
        return form

    def get(self, request):
        identifier = dict(request.GET.lists())["topic_list"] \
            if "topic_list" in request.GET else None
        if type(identifier) is list:
            identifier = identifier[0]
        seed = self.get_seed()
        theme = self._get_current_theme(request)
        topics = theme.get_topics_from_identifier(identifier)
        question = api.get_random_question_from_topics(topics, seed)
        form = self._get_form_from_question(question)
        json_question = question.model_dump_json()
        topic_form = self._get_topic_form(theme, identifier)
        context_dict = {
            "question": question,
            "json_question": json_question,
            "form": form,
            "topic_form": topic_form,
            "topic_list": topics
        }
        return render(request, self.template_name, context_dict)






