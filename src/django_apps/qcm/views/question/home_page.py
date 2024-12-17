from.base_view import AbstractQuestionView
from datetime import date


class DailyQuestionView(AbstractQuestionView):
    template_name = 'qcm/home-page.html'
    TOPICS = ["AMM", "AMM/Fauna", "AMM/Flora", "AMM/Toponymie", "AMM/Le milieu montagnard",
              "AMM/La profession d’AMM, son environnement géographique, institutionnel et réglementaire",
              "AMM/Milieu montagnard enneigé", "AMM/Milieu montagnard tropical et équatorial"]

    def get_seed(self) -> str | int | float | None:
        today = date.today()
        year_week = today.isocalendar()[:2]
        week_seed = '-'.join([str(_) for _ in year_week])
        return week_seed

    def get_default_topic(self) -> str:
        # return "AMM/Fauna"
        today = date.today()
        day_number = today.weekday()
        return DailyQuestionView.TOPICS[day_number]

    def get_topic_list(self) -> list[str]:
        return DailyQuestionView.TOPICS
