from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models.groups.Model_group import Group
from .models.lessons import Lesson, LessonMain, Exam, ExamSubmission, StudentGrade, HomeWork, HomeworkGrade, \
    HomeworkSubmission, StudentAbsentOrCame
from .models.news import NewsModels
from .models.roles.models_roles import User
from .models.departaments.departaments import TeacherDepartment
from .models.students import StudentLanguage, StudentProfile
from .models.workers.mentor_model import MentorProfile
from .models.workers.teacher_model import TeacherProfile


class UserAdminForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role', 'age', 'is_staff', 'is_superuser')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'age')

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Пароли не совпадают")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'age', 'password', 'is_active', 'is_staff', 'is_superuser')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role', 'age')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'age', 'password1', 'password2'),
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(NewsModels)
admin.site.register(Lesson)
admin.site.register(LessonMain)
admin.site.register(Exam)
admin.site.register(ExamSubmission)
admin.site.register(StudentGrade)
admin.site.register(HomeWork)
admin.site.register(HomeworkGrade)
admin.site.register(HomeworkSubmission)
admin.site.register(StudentAbsentOrCame)
admin.site.register(StudentLanguage)
admin.site.register(StudentProfile)
admin.site.register(MentorProfile)
admin.site.register(TeacherProfile)
admin.site.register(Group)
admin.site.register(TeacherDepartment)
