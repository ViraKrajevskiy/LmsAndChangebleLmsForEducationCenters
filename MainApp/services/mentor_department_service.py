from .base import BaseService
from MainApp.models.departaments.departaments import MentorDepartment
from ..models.Workers.mentor_model import MentorProfile

class MentorDepartmentService(BaseService):
    model = MentorDepartment

class MentorProfileService(BaseService):
    model = MentorProfile