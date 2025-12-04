from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models

from MainApp.validators.file_photo_validators import validate_file_extension


class Exam(models.Model):
    lesson = models.ForeignKey("Lesson", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher = models.ForeignKey("TeacherProfile", on_delete=models.CASCADE)
    max_grade = models.FloatField(default=100.0)

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Время начала экзамена должно быть раньше времени окончания.")

        # Проверяем пересечения по времени для этого учителя
        exams_same_day = Exam.objects.filter(
            date=self.date,
            teacher=self.teacher
        ).exclude(id=self.id)

        for exam in exams_same_day:
            if (self.start_time < exam.end_time) and (self.end_time > exam.start_time):
                raise ValidationError(
                    f"Экзамен пересекается по времени с экзаменом «{exam.title}» "
                    f"({exam.start_time}–{exam.end_time})."
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} — {self.date} ({self.start_time}-{self.end_time})"


class ExamSubmission(models.Model):
    student = models.ForeignKey("StudentProfile", on_delete=models.CASCADE)
    exam = models.ForeignKey("Exam", on_delete=models.CASCADE)
    file = models.FileField(
        upload_to="exam_submissions/",
        validators=[validate_file_extension],
        null=True,
        blank=True
    )    
    photo = models.ImageField(upload_to='exam_submissions/', blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'exam')
        verbose_name = "Ответ студента на экзамен"
        verbose_name_plural = "Ответы студентов на экзамены"

    def clean(self):
        # Проверка дедлайна: нельзя сдавать после конца экзамена
        exam_end = timezone.datetime.combine(self.exam.date, self.exam.end_time)
        if timezone.now() > exam_end:
            raise ValidationError("Срок сдачи экзамена истёк. Вы не можете загрузить ответ.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.user.username} — {self.exam.title}"
