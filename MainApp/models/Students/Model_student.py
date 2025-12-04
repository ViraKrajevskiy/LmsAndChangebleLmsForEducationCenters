from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from MainApp.models.roles.models_roles import User
from django.core.exceptions import ValidationError

from MainApp.validators.phone_number_validator import phone_validator


class StudentLanguage(models.Model):
    language = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.language}'

class StudentLanguageLevel(models.Model):
    LEVEL_CHOICES = [
        ('native', 'Родной'),
        ('excellent', 'Отлично'),
        ('medium', 'Средне'),
        ('basic', 'Базово'),
    ]

    student = models.ForeignKey("StudentProfile", on_delete=models.CASCADE, related_name='languages_with_levels')
    language = models.ForeignKey(StudentLanguage, on_delete=models.CASCADE)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)

    class Meta:
        unique_together = ('student', 'language')  # один язык — один уровень

    def __str__(self):
        return f"{self.student.user.username}: {self.language} ({self.get_level_display()})"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_phone = models.CharField(
        max_length=13,
        blank=True,
        validators=[phone_validator]
    )
    parent_name = models.CharField(max_length=150, blank=True)
    parent_phone = models.CharField(
        max_length=13,
        blank=True,
        validators=[phone_validator]
    )
    studentknowlanguage = models.ManyToManyField(StudentLanguage, related_name='students')
    course = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    group = models.ForeignKey("Group",on_delete=models.SET_NULL,null=True,related_name='students')

    def clean(self):
        if self.user.role != 'student':
            raise ValidationError("Профиль студента можно создать только для роли student.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} — {self.group}"
