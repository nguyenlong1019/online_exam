from django.shortcuts import render, redirect 
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from quiz.models.quiz import Exam, Monitor 
from django.http import Http404, HttpResponse
import subprocess 


@csrf_exempt
def upload_video(request, pk):
    try:
        exam = Exam.objects.get(pk=pk)
    except Exam.DoesNotExist:
        return Http404() 

    if request.method == 'POST' and 'video_recording' in request.FILES:
        print(request.FILES)
        video_file = request.FILES['video_recording']
        
        file_size = video_file.size
        print(f"Dung lượng của file: {file_size} bytes")

        user = request.user 

        monitor = Monitor(
            user=user,
            exam=exam
        )
        webm_path = f"{user.id}_{exam.id}_recorded_video.webm"
        monitor.video.save(webm_path, video_file)
        monitor.save()
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)


def monitor_list_view(request):
    if request.user.is_authenticated and request.user.has_perm('quiz.view_teacherprofile'):
        exams = Exam.objects.order_by('-created_at')
        return render(request, 'quiz/monitor.html', {'exams': exams}, status=200)
    else:
        return HttpResponse('<h1>404 Not Found</h1>', status=404)


def monitor_detail_view(request, pk):
    if request.user.is_authenticated and request.user.has_perm('quiz.view_teacherprofile'):
        try:
            exam = Exam.objects.get(pk=pk)
        except Exam.DoesNotExist:
            return HttpResponse('<h1>404 Not Found</h1>', status=404)

        monitors = Monitor.objects.filter(exam=exam)
        return render(request, 'quiz/monitor-detail.html', {'monitors': monitors, 'exam': exam}, status=200)
    else:
        return HttpResponse('<h1>404 Not Found</h1>', status=404)

