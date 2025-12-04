from MainApp.models.Lessons.exam.exams import ExamSubmission, Exam
from .base import BaseService

class ExamSubmissionService(BaseService):
    model = ExamSubmission
    allowed_roles = ["student", "mentor", "teacher"]
    user_field_name = "student"

class ExamService(BaseService):
    model = Exam
    allowed_roles = ["student", "teacher", "mentor"]
