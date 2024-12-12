from pydantic import BaseModel, Field
from pathlib import Path
from qa import resource_dir_path
from qa.mcq_db.models import MCQData
import json

reports_json_file: Path = resource_dir_path / "problems.json"


class QuestionReport(BaseModel):
    mcq_context: MCQData
    report: str
    answers: list[str] = Field(default_factory=list)


class QuestionReports(BaseModel):
    hash: str
    reports: list[QuestionReport] = Field(default_factory=list)

    def already_exists(self, report: QuestionReport) -> bool:
        for _ in self.reports:
            if _.report == report.report:
                return True
        return False


class DictOfQuestionReports(BaseModel):
    problems: dict[str, QuestionReports] = Field(default_factory=dict)

    def add_report(self, report: QuestionReport, save: bool = True):
        if report.mcq_context.hash() not in self.problems:
            self.problems[report.mcq_context.hash()] = QuestionReports(hash=report.mcq_context.hash())
        if self.problems[report.mcq_context.hash()].already_exists(report):
            return
        self.problems[report.mcq_context.hash()].reports.append(report)
        if save:
            self.save()

    def get_reports_from_mcq(self, mcq: MCQData) -> QuestionReports | None:
        if (mcq_hash := mcq.hash()) in self.problems:
            return self.problems[mcq_hash]
        return None

    def save(self):
        json_model = self.model_dump()
        with open(reports_json_file, "w") as f:
            f.write(json.dumps(json_model, indent=2, ensure_ascii=False))


def get_dict_problems():
    with open(reports_json_file, "r", encoding='utf-8') as f:
        json_data = json.loads(f.read())
    return DictOfQuestionReports(**json_data)
