from django.core.exceptions import ValidationError
from django.db import models

class LessonMain(models.Model):
    lesson_day = models.DateField()
    group = models.ForeignKey("Group", on_delete=models.CASCADE)  # расписание для группы

    def __str__(self):
        return f"Расписание {self.group.name} — {self.lesson_day}"

class Lesson(models.Model):
    LESSON_TYPE = [
        ('lecture', 'Лекция'),
        ('practice', 'Практика'),
        ('lab', 'Лабораторная'),
    ]
    main = models.ForeignKey(LessonMain,on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=50)
    lesson_topick = models.TextField(max_length=200)
    teacher = models.ForeignKey("User", on_delete=models.CASCADE,
                                limit_choices_to={'role': 'teacher'}, related_name='lessons_as_teacher')
    mentor = models.ForeignKey("User",on_delete=models.CASCADE,related_name='lessons_as_mentor')
    lesson_type = models.CharField(max_length=20,choices=LESSON_TYPE,default='lecture')
    start_time = models.TimeField()
    end_time = models.TimeField()

    def clean(self):
        # Проверяем что начало < конца
        if self.start_time >= self.end_time:
            raise ValidationError("Время начала урока должно быть раньше времени окончания.")
        # Берём все уроки из этого же дня и группы
        lessons_same_day = Lesson.objects.filter(
            main=self.main
        ).exclude(id=self.id)

        for lesson in lessons_same_day:
            # Пересечение по времени
            if (self.start_time < lesson.end_time) and (self.end_time > lesson.start_time):
                raise ValidationError(
                    f"Урок пересекается по времени с уроком «{lesson.title}» "
                    f"({lesson.start_time}–{lesson.end_time})."
                )

    def save(self, *args, **kwargs):
        self.clean()   # обязательно вызывать clean() при сохранении
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_lesson_type_display()})"
