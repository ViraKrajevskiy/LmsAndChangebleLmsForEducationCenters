from django.db import models

class NewsModels(models.Model):
    title = models.CharField()
    text_topick = models.TextField()
    date_field = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField()
    file = models.FileField()
    
    def __str__(self):
        return self.title, self.date_field , self.photo
    