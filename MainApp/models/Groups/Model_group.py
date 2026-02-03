from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.name}'

    @property
    def student_count(self):
        return self.students.count()
 