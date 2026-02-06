from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from MainApp.models import HomeWork, StudentProfile, HomeworkSubmission, HomeworkGrade

def homework_detail(request, pk):
    # 1. Получаем задание
    homework = get_object_or_404(HomeWork, pk=pk)

    # 2. Получаем профиль студента
    student_profile = get_object_or_404(StudentProfile, user=request.user)

    # 3. Ищем сдачу работы (файл, фото, комментарий студента)
    submission = HomeworkSubmission.objects.filter(
        student=student_profile,
        homework=homework
    ).first()

    # 4. Ищем ОЦЕНКУ (ИСПРАВЛЕНО: ищем через student и homework)
    grade = HomeworkGrade.objects.filter(
        student=student_profile,
        homework=homework
    ).first()

    # 5. Обработка отправки (POST)
    if request.method == 'POST':
        file = request.FILES.get('file')
        photo = request.FILES.get('photo')
        comment = request.POST.get('comment', '').strip()

        if submission:
            # Обновляем старую сдачу
            if file: submission.file = file
            if photo: submission.photo = photo
            submission.comment = comment
            submission.save()
            messages.success(request, "Работа успешно обновлена!")
        else:
            # Создаем новую сдачу
            HomeworkSubmission.objects.create(
                student=student_profile,
                homework=homework,
                file=file,
                photo=photo,
                comment=comment
            )
            messages.success(request, "Работа отправлена на проверку!")

        return redirect('homework_detail', pk=pk)

    # 6. Рендерим страницу
    return render(request, 'student/homework_detail.html', {
        'homework': homework,
        'submission': submission,
        'grade': grade, # Теперь это работает без ошибок
    })