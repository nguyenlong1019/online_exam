from django.shortcuts import render, redirect 
from django.contrib.auth import login, authenticate, logout 
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required 
from quiz.models.quiz import Exam 
from django.contrib import messages 


def index_view(request):
    exams = Exam.objects.order_by('-created_at')
    if request.user.is_authenticated:
        user = User.objects.filter(username=request.user.username)
        if user.exists():
            user = user.first()
            if user.has_perm('quiz.add_teacherprofile'):
                try:
                    exams = Exam.objects.filter(created_by=user.teacherprofile)
                except Exception as e:
                    print(str(e))
                    pass 
            elif user.has_perm('quiz.view_studentprofile'):
                try:
                    exams = Exam.objects.filter(classroom=user.studentprofile.classroom)
                except Exception as e:
                    print(str(e))
                    pass 
    
    return render(request, 'quiz/index.html', {'exams': exams}, status=200)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username đã tồn tại')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email đã tồn tại')
            return redirect('register')
        
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )
        user.is_staff = True 
        user.save()

        return redirect('login')


    return render(request, 'quiz/register.html', status=200)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Sai tên đăng nhập hoặc mật khẩu')
    
    return render(request, 'quiz/login.html', status=200)


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('login')


