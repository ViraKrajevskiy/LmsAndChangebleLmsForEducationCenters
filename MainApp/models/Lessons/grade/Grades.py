from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class StudentGrade(models.Model):
    student = models.ForeignKey("StudentProfile",on_delete=models.CASCADE)
    lesson = models.ForeignKey("Lesson",on_delete=models.CASCADE)
    grade = models.FloatField(validators=[MinValueValidator(0.0),MaxValueValidator(100.0)])
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('student','lesson')
        verbose_name = "Оценка студента"
        verbose_name_plural = "Оценки студентов"

    def __str__(self):
        return f"{self.student.user.username}-{self.grade}/100"


class HomeworkGrade(models.Model):
    student = models.ForeignKey("StudentProfile", on_delete=models.CASCADE)
    homework = models.ForeignKey("HomeWork", on_delete=models.CASCADE)
    grade = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'homework')
        verbose_name = "Оценка за ДЗ"
        verbose_name_plural = "Оценки за ДЗ"

    def __str__(self):
        return f"{self.student.user.username} — {self.grade}/100"


# так смотри нам нужен орм для моделей я скажу щя каким ролям что можно пока просто нужно орм удаление изменение создание просмотр