from django.db import models

class StudentAbsentOrCame(models.Model):
    STATUS_CHOICES = [
        ('Absent','Отсутствует'),
        ('Late','Опоздал'),
        ('Present','Присутствует'),
        ('Problem_with_health','Проблемы со здоровьем'),
        ('Family_problem','По семейным обстоятельствам'),
    ]
    student = models.ForeignKey("StudentProfile", on_delete=models.CASCADE)
    lesson = models.ForeignKey("Lesson", on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.user.username}: {self.status} ({self.lesson})"