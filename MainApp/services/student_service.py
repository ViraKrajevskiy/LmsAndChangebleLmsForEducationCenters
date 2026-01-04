from django.core.exceptions import PermissionDenied

from .base import BaseService
from ..models import StudentGrade, StudentAbsentOrCame, StudentLanguage, StudentProfile

class StudentProfileService(BaseService):
    model = StudentProfile
    allowed_roles = ["student", "teacher", "mentor"]
    user_field_name = "user"


class StudentLanguageService(BaseService):
    model = StudentLanguage
    allowed_roles = ["student", "teacher", "mentor"]
    user_field_name = "students"

    @classmethod
    def create(cls, user, **data):
        raise PermissionDenied("Создавать языки нельзя через этот сервис.")

    @classmethod
    def update(cls, user, obj_id, **data):
        obj = cls.model.objects.get(id=obj_id)
        if user.role == "student":
            if user.studentprofile not in obj.students.all():
                raise PermissionDenied("Студент может менять только свои языки.")
            return super().update(user, obj_id, **data)
        else:
            raise PermissionDenied("Только студент может менять свои языки.")

    @classmethod
    def delete(cls, user, obj_id):
        raise PermissionDenied("Удалять языки нельзя через этот сервис.")

class StudentAbsentService(BaseService):
    model = StudentAbsentOrCame
    allowed_roles = ["student", "mentor", "teacher"]
    user_field_name = "student"

    @classmethod
    def create(cls, user, **data):
        if user.role != "teacher":
            raise PermissionDenied("Только учитель может отмечать посещаемость студента.")
        return super().create(user, **data)

    @classmethod
    def update(cls, user, obj_id, **data):
        if user.role != "teacher":
            raise PermissionDenied("Только учитель может изменять посещаемость студента.")
        return super().update(user, obj_id, **data)

    @classmethod
    def delete(cls, user, obj_id):
        if user.role != "teacher":
            raise PermissionDenied("Только учитель может удалять записи посещаемости.")
        return super().delete(user, obj_id)

class StudentGradeService(BaseService):
    model = StudentGrade
    allowed_roles = ["teacher", "mentor"]
    user_field_name = "student"


