from django.db import models

class NewsModels(models.Model):
    title = models.CharField(max_length=200)
    text_topick = models.TextField()
    date_field = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)

   
    USER_TYPES_CHOICES = (
        ('all', 'Для всех'),
        ('student', 'Только для студентов'),
        ('mentor', 'Только для менторов'),
        ('teacher', 'Только для учителей'),
    )


    user_role = models.CharField(
        max_length=20,
        choices=USER_TYPES_CHOICES,
        default='all'
    )

    def __str__(self):
        return f"{self.title} | {self.date_field}"