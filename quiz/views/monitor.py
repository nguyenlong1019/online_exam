from django.shortcuts import render, redirect 
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from quiz.models.quiz import Exam, Monitor 
from django.http import Http404 
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
        # file_path = os.path.join('videos', 'recorded_video.webm')

        # Kiểm tra dung lượng của file
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

        # webm_full_path = os.path.join(settings.MEDIA_ROOT, 'video', webm_path)
        # mp4_path = webm_full_path.replace('.webm', '.mp4')
        # convert_command = ["ffmpeg", "-i", webm_full_path, "-c:v", "libx264", "-c:a", "aac", "-strict", "experimental", mp4_path]

        # # Thực thi lệnh chuyển đổi
        # subprocess.run(convert_command)

        # # Lưu lại đường dẫn của file mp4
        # monitor.video.name = mp4_path.replace(settings.MEDIA_ROOT + "/", "")  # Cập nhật trường video với file .mp4
        # monitor.save()
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)


def monitor_list_view(request):
    exams = Exam.objects.order_by('-created_at')
    return render(request, 'quiz/monitor.html', {'exams': exams}, status=200)


def monitor_detail_view(request, pk):
    try:
        exam = Exam.objects.get(pk=pk)
    except Exam.DoesNotExist:
        return Http404()

    monitors = Monitor.objects.filter(exam=exam)
    return render(request, 'quiz/monitor-detail.html', {'monitors': monitors, 'exam': exam}, status=200)

