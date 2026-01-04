from .base import BaseService
from ..models import MentorProfile, TeacherDepartment


class MentorDepartmentService(BaseService):
    model = TeacherDepartment

class MentorProfileService(BaseService):
    model = MentorProfile