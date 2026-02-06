{% extends 'base_menu/base.html' %}
{% load static %}

{% block title %}{{ lesson.title }} | LMS PRO{% endblock %}

{% block content %}
<link rel="stylesheet" href="{% static 'css/student/lesson_detail.css' %}">

<div class="container py-4">
    <nav aria-label="breadcrumb" class="mb-4">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="{% url 'full_schedule' %}">Расписание</a></li>
            <li class="breadcrumb-item active text-navy fw-bold" aria-current="page">{{ lesson.title }}</li>
        </ol>
    </nav>

    {% if messages %}
        <div class="messages-container">
            {% for message in messages %}
                <div class="alert {% if message.tags == 'error' %}alert-danger{% else %}alert-success{% endif %} alert-dismissible fade show rounded-4 shadow-sm mb-4" role="alert">
                    <i class="bi {% if message.tags == 'error' %}bi-exclamation-octagon{% else %}bi-check-circle{% endif %} me-2"></i>
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            {% endfor %}
        </div>
    {% endif %}

    <div class="row g-4">
        <div class="col-lg-8">
            <div class="card border-0 shadow-sm rounded-4 mb-4">
                <div class="card-body p-4">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                        <div>
                            <span class="badge bg-primary-subtle text-primary mb-2">
                                {{ lesson.get_lesson_type_display }}
                            </span>
                            <h2 class="fw-bold text-navy mb-0">{{ lesson.title }}</h2>
                        </div>
                        <div class="text-end">
                            <div class="h4 fw-bold text-primary mb-0">{{ lesson.start_time|time:"H:i" }}</div>
                            <div class="small text-muted">до {{ lesson.end_time|time:"H:i" }}</div>
                        </div>
                    </div>

                    <hr class="my-4 opacity-25">

                    <h5 class="fw-bold text-navy mb-3">Тема занятия:</h5>
                    <div class="lesson-topic-text">
                        {{ lesson.lesson_topick|linebreaks|default:"Тема не указана" }}
                    </div>
                </div>
            </div>

            <div class="card border-0 shadow-sm rounded-4 mb-4">
                <div class="card-body p-4">
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <h5 class="fw-bold text-navy mb-0">
                            <i class="bi bi-cloud-arrow-up me-2"></i>Материалы урока
                        </h5>
                        <span class="badge {% if materials.count >= 3 %}bg-danger{% else %}bg-primary{% endif %} rounded-pill">
                            Файлов: {{ materials.count }} / 3
                        </span>
                    </div>

                    {% if materials.count < 3 %}
                        <form method="post" enctype="multipart/form-data" class="bg-light p-3 rounded-4 mb-4 border border-dashed" id="uploadForm">
                            {% csrf_token %}
                            <div class="row g-2">
                                <div class="col-md-5">
                                    <input type="text" name="title" class="form-control form-control-sm rounded-3" placeholder="Название (напр. Практика)" required>
                                </div>
                                <div class="col-md-5">
                                    <input type="file" name="file" class="form-control form-control-sm rounded-3" required>
                                </div>
                                <div class="col-md-2">
                                    <button type="submit" class="btn btn-primary btn-sm w-100 rounded-3 shadow-sm">
                                        Загрузить
                                    </button>
                                </div>
                            </div>
                        </form>
                    {% else %}
                        <div class="alert alert-warning border-0 rounded-4 small mb-4">
                            <i class="bi bi-info-circle me-2"></i>
                            Лимит загрузок (3 файла) исчерпан.
                        </div>
                    {% endif %}

                    {% if materials %}
                        <h6 class="fw-bold text-navy small mb-3">Ваши загрузки:</h6>
                        <div class="list-group list-group-flush">
                            {% for m in materials %}
                            <div class="list-group-item d-flex justify-content-between align-items-center bg-transparent px-0 border-bottom">
                                <div class="d-flex align-items-center">
                                    <div class="bg-primary-subtle text-primary rounded-3 p-2 me-3">
                                        <i class="bi bi-file-earmark-arrow-up fs-5"></i>
                                    </div>
                                    <div>
                                        <div class="small fw-bold text-navy">{{ m.title|default:"Файл без названия" }}</div>
                                        <div class="text-muted" style="font-size: 10px;">{{ m.uploaded_at|date:"d M, H:i" }}</div>
                                    </div>
                                </div>
                                <a href="{{ m.file.url }}" class="btn btn-sm btn-light border rounded-pill px-3 shadow-sm" target="_blank">
                                    <i class="bi bi-eye me-1"></i> Посмотреть
                                </a>
                            </div>
                            {% endfor %}
                        </div>
                    {% else %}
                        <div class="text-center py-4 border rounded-4 border-dashed bg-light bg-opacity-50">
                            <i class="bi bi-folder-plus display-6 text-muted mb-2 d-block"></i>
                            <small class="text-muted">Вы еще не загружали файлы</small>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>

        <div class="col-lg-4">
            <div class="card border-0 shadow-sm rounded-4 mb-4">
                <div class="card-body p-4">
                    <h5 class="fw-bold text-navy mb-4">Организаторы</h5>
                    <div class="d-flex align-items-center mb-4">
                        <div class="avatar-circle bg-success-subtle text-success me-3">
                            <i class="bi bi-person-badge"></i>
                        </div>
                        <div>
                            <div class="small text-muted">Преподаватель</div>
                            <div class="fw-bold text-navy">{{ lesson.teacher.get_full_name|default:lesson.teacher.username }}</div>
                        </div>
                    </div>
                    <div class="d-flex align-items-center">
                        <div class="avatar-circle bg-info-subtle text-info me-3">
                            <i class="bi bi-person-video3"></i>
                        </div>
                        <div>
                            <div class="small text-muted">Ментор</div>
                            <div class="fw-bold text-navy">{{ lesson.mentor.get_full_name|default:lesson.mentor.username }}</div>
                        </div>
                    </div>
                </div>
            </div>

            {% if homeworks %}
                <div class="card border-0 shadow-sm rounded-4 border-start border-4 border-warning">
                    <div class="card-body p-4">
                        <h6 class="fw-bold text-navy mb-3">
                            <i class="bi bi-journal-check me-2 text-warning"></i>Связано с ДЗ:
                        </h6>
                        {% for hw in homeworks %}
                            <a href="{% url 'homework_detail' hw.id %}" class="text-decoration-none d-block p-3 bg-warning-subtle rounded-4 mb-2 transition-hover">
                                <div class="small fw-bold text-warning-emphasis mb-1">{{ hw.title }}</div>
                                <div class="d-flex justify-content-between align-items-center">
                                    <span class="text-muted" style="font-size: 11px;">
                                        <i class="bi bi-calendar-x me-1"></i>До {{ hw.dedline|date:"d.m, H:i" }}
                                    </span>
                                    <i class="bi bi-chevron-right text-warning small"></i>
                                </div>
                            </a>
                        {% endfor %}
                    </div>
                </div>
            {% endif %}
        </div>
    </div>
</div>

<script src="{% static 'js/lesson_detail.js' %}"></script>
{% endblock %}