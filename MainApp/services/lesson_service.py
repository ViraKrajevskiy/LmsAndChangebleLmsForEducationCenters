from .base import BaseService
from ..models import Lesson, LessonMain


class LessonService(BaseService):
    model = Lesson
    allowed_roles = ["student", "teacher", "mentor"]


class LessonMainService(BaseService):
    model = LessonMain
    allowed_roles = ["student", "teacher", "mentor"]
    