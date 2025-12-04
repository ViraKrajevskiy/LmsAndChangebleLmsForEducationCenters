from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # Редирект по роли
            if user.is_teacher():
                return redirect("profile")
            if user.is_student():
                return redirect("profile")
            if user.is_mentor():
                return redirect("profile")
            print("AUTH:", user)

            return redirect("profile")  # fallback
        print("AUTH:", user)
        return render(request, "auth/login.html", {"error": "Неверный логин или пароль"})
    
    return render(request, "auth/login.html")


