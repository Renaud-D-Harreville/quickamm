from django.shortcuts import render
from django.views import View
from django_apps.qcm.forms import QCMForm, TopicForm
from qa.mcq_db.models import MCQData
from qa.api import api
from pydantic import BaseModel
from qa.topics.themes import Theme

class TopicFormInformation(BaseModel):
    name: str
    value: str
    label: str
    label_id: str
    has_sub_themes: bool
    checked: bool


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

    def _set_current_theme(self, request, theme: Theme):
        request.session['current_theme'] = theme.model_dump()
        request.session.modified = True  # Indiquer que la session a été modifiée

    def get_seed(self) -> str | int | float | None:
        return None

    @staticmethod
    def _get_form_from_question(question: MCQData) -> QCMForm:
        form = QCMForm()
        form.fields['question'].initial = question.model_dump()
        form.fields['text_answers'].choices = [(index, answer) for index, answer in
                                               enumerate(question.answers)]
        return form

    # def _get_choices_from_theme(self, theme: Theme) -> list[tuple[str, str, dict]]:
    #     main_theme_choice = (theme.identifier, theme.name, {'has_sub_themes': True})
    #     if theme.sub_themes is None:
    #         return [main_theme_choice]
    #     sub_themes_choices = [(sub_theme.identifier, f" > {sub_theme.name}", {'has_sub_themes': theme.sub_themes is not None})
    #                           for _, sub_theme in theme.sub_themes.items()]
    #     return [main_theme_choice] + sub_themes_choices
    #
    # def _get_topic_form(self, theme: Theme, initial: str = None) -> TopicForm:
    #     if initial is None:
    #         initial = theme.identifier
    #     form = TopicForm()
    #     form.set_topic_choices(theme, initial)
    #     return form

    def _get_topic_form_information(self, theme: Theme, initial: str, index: int) -> TopicFormInformation:
        name = 'topic_list'
        value = theme.identifier
        label =  theme.name
        label_id = f"{name}_{index}"
        has_sub_themes = theme.sub_themes is not None
        checked = initial == theme.identifier
        return TopicFormInformation(
            name=name,
            value=value,
            label=label,
            label_id=label_id,
            has_sub_themes=has_sub_themes,
            checked=checked
        )

    def _get_topic_form_information_list(self, theme: Theme, initial: str) -> list[TopicFormInformation]:
        if initial is None:
            initial = theme.identifier
        l = []
        main_theme_info = self._get_topic_form_information(theme, initial, 0)
        l.append(main_theme_info)
        for i, sub_theme in enumerate(theme.sub_themes.values()):
            l.append(self._get_topic_form_information(sub_theme, initial, i + 1))
        return l

    def get_context(self, theme: Theme, identifier: str) -> dict:
        seed = self.get_seed()
        topics = theme.get_topics_from_identifier(identifier)
        question = api.get_random_question_from_topics(topics, seed)
        form = self._get_form_from_question(question)
        json_question = question.model_dump_json()
        topic_form = self._get_topic_form_information_list(theme, identifier)
        context_dict = {
            "question": question,
            "json_question": json_question,
            "form": form,
            "topic_form": topic_form,
            "topic_list": topics
        }
        return context_dict

    def _retrieve_identifier(self, query_dict):
        identifier = dict(query_dict.lists())["identifier"] \
            if "identifier" in query_dict else None
        if type(identifier) is list:
            identifier = identifier[0]

        return identifier

    def get(self, request):  # get leave the theme as it

        identifier = self._retrieve_identifier(request.GET)
        theme = self._get_current_theme(request)
        context_dict = self.get_context(theme, identifier)
        return render(request, self.template_name, context_dict)


    def post(self, request):  # The post change the theme according to the identifier
        identifier = self._retrieve_identifier(request.POST)
        current_theme = self._get_current_theme(request)
        new_theme = api.get_sub_theme(current_theme, identifier)
        self._set_current_theme(request, new_theme)

        context_dict = self.get_context(new_theme, identifier)
        return render(request, self.template_name, context_dict)














