from django.db import models

class NewsModels(models.Model):
    title = models.CharField()
    text_topick = models.TextField()
    date_field = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField()
    file = models.FileField()
    
    USER_TYPES = (
        ('all', 'Для всех'),
        ('student', 'Только для студентов'),
        ('mentor', 'Только для менторов'),
        ('teacher', 'Только для учителей'),
    )

    def __str__(self):
        return self.title, self.date_field , self.photo
    