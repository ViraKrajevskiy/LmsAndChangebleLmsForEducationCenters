from django.db import models
from django.core.exceptions import ValidationError
from MainApp.models.departaments.departaments import TeacherDepartment
from MainApp.models.roles.models_roles import User
from MainApp.validators.phone_number_validator import phone_validator


class MentorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='mentor_profile'
    )
    specialization = models.CharField(max_length=60)
    department = models.ForeignKey(
        TeacherDepartment,
        on_delete=models.SET_NULL,
        null=True,
        related_name='teacherses'
    )
    mentor_phone = models.CharField(
        max_length=13,
        blank=True,
        validators=[phone_validator]
    )
    bio = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    def clean(self):
        if self.user.role != 'mentor':
            raise ValidationError("MentorProfile доступен только для пользователей с ролью mentor.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.specialization}"
