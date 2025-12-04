from django.db import models
from django.core.exceptions import ValidationError
from MainApp.models.departaments.departaments import TeacherDepartment
from MainApp.models.roles.models_roles import User
from MainApp.validators.phone_number_validator import phone_validator


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    mentor_phone = models.CharField(
        max_length=13,
        blank=True,
        validators=[phone_validator]
    )
    bio = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    specialization = models.CharField(max_length=60)
    department = models.ForeignKey(
        TeacherDepartment,
        on_delete=models.SET_NULL,
        null=True,
        related_name='teachers'
    )

    def clean(self):
        if self.user.role != 'teacher':
            raise ValidationError("TeacherProfile доступен только для пользователей с ролью teacher.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.specialization}"
