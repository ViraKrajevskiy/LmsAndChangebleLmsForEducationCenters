from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from MainApp.models import Lesson, HomeWork, StudentProfile, LessonMain
from MainApp.models.lessons.lesson_main.Main_lesson_Model import LessonMaterial


@login_required
def full_schedule_view(request):
    student_profile = StudentProfile.objects.filter(user=request.user).first()


    if not student_profile:
        return render(request, 'student/full_schedule.html', {'error': 'Профиль не найден'})

    schedule_days = LessonMain.objects.filter(
        group=student_profile.group
    ).order_by('lesson_day').prefetch_related('lessons')

    return render(request, 'student/full_schedule.html', {
        'schedule_days': schedule_days,
        'group': student_profile.group
    })

@login_required
def lesson_detail_view(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    student = request.user.studentprofile


    materials = LessonMaterial.objects.filter(lesson=lesson, student=student)

    if request.method == 'POST':
        if not lesson.can_upload:
            messages.error(request, "Для этого занятия загрузка файлов отключена.")
            return redirect('lesson_detail', pk=pk)
        if materials.count() >= 3:
            messages.error(request, "Ошибка: Максимальное количество загрузок для этого урока (3 файла) достигнуто.")
            return redirect('lesson_detail', pk=pk)


        title = request.POST.get('title')
        file = request.FILES.get('file')

        if file:
            LessonMaterial.objects.create(
                lesson=lesson,
                student=student,
                title=title,
                file=file
            )
            messages.success(request, "Файл успешно загружен!")
            return redirect('lesson_detail', pk=pk)

    homeworks = HomeWork.objects.filter(lesson=lesson)

    return render(request, 'student/lesson_detail.html', {
        'lesson': lesson,
        'homeworks': homeworks,
        'materials': materials,
    })