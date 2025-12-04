from MainApp.models.Lessons.HomeWork.Hw_model_main import HomeworkSubmission,HomeWork
from MainApp.models.Lessons.grade.Grades import HomeworkGrade
from MainApp.services.base import BaseService

class HomeworkService(BaseService):
    model = HomeWork
    allowed_roles = ["student", "teacher", "mentor"]
    user_field_name = "student"

class HomeworkSubmissionService(BaseService):
    model = HomeworkSubmission
    allowed_roles = ["student"]

class HomeworkGradeService(BaseService):
    model = HomeworkGrade
    allowed_roles = ["teacher", "mentor"]
    user_field_name = "student"