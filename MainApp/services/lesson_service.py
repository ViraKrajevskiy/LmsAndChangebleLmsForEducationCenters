from .base import BaseService
from ..models.Lessons.Lesson_Main.Main_lesson_Model import Lesson, LessonMain

class LessonService(BaseService):
    model = Lesson
    allowed_roles = ["student", "teacher", "mentor"]


class LessonMainService(BaseService):
    model = LessonMain
    allowed_roles = ["student", "teacher", "mentor"]
    