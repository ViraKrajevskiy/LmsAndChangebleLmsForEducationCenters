from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from MainApp.validators.file_photo_validators import validate_file_extension


class HomeWork(models.Model):
    lesson = models.ForeignKey("Lesson",on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    topic = models.TextField(blank=False)
    photo = models.ImageField(upload_to='student_photos/',blank=True, null=True)
    file = models.FileField(upload_to="homework_submissions/",
                            validators=[validate_file_extension],
                            null=True, blank=True)
    dedline = models.DateTimeField()
    allow_late = models.BooleanField(
        default=False,
        help_text="Разрешить студентам сдавать ДЗ после дедлайна"
    )

class HomeworkSubmission(models.Model):
    student = models.ForeignKey("StudentProfile", on_delete=models.CASCADE)
    homework = models.ForeignKey("HomeWork", on_delete=models.CASCADE)
    file = models.FileField(upload_to="homework_submissions/",
                        validators=[validate_file_extension],
                            null=True, blank=True)
    photo = models.ImageField(upload_to='homework_submissions/', blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'homework')
        verbose_name = "Задание студента"
        verbose_name_plural = "Задания студентов"

    def clean(self):
        
        if not self.homework.allow_late and self.homework.dedline < timezone.now():
            raise ValidationError("Срок сдачи ДЗ истёк. Поздняя сдача запрещена.")

    def save(self, *args, **kwargs):
        self.clean()  # вызываем проверку перед сохранением
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.user.username} — {self.homework.title}"



