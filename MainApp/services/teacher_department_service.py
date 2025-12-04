from .base import BaseService
from MainApp.models.departaments.departaments import TeacherDepartment
from ..models.Workers.teacher_model import TeacherProfile

class TeacherDepartmentService(BaseService):
    model = TeacherDepartment

class TeacherProfileService(BaseService):
    model = TeacherProfile