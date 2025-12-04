from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Username обязателен")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'teacher')  # можно любая роль
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('teacher', 'Учитель'),
        ('mentor', 'Ментор'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    age = models.PositiveIntegerField(null=True, blank=True)

    objects = UserManager()

    def is_student(self):
        return self.role == 'student'

    def is_teacher(self):
        return self.role == 'teacher'

    def is_mentor(self):
        return self.role == 'mentor'

    def clean(self):
        super().clean()

        if self.email:
            domain = self.email.split('@')[-1]
            if domain in BAD_DOMAINS:
                raise ValidationError("Email не может быть с временного сервиса.")


BAD_DOMAINS = ['tempmail.com', 'quickmail.xyz', 'trashmail.net']