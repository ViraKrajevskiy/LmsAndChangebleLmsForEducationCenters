from django import forms

from MainApp.models.lessons.lesson_main.Main_lesson_Model import LessonMaterial


class LessonMaterialForm(forms.ModelForm):
    class Meta:
        model = LessonMaterial
        fields = ['file', 'title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название (например: Классная работа)'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }