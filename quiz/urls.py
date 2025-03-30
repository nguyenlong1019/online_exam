from django.urls import path 
from quiz.views.index import * 
from quiz.views.quiz import * 
from quiz.views.monitor import * 


urlpatterns = [
    path('', index_view, name='index'), # home page 
    path('login/', login_view, name='login'), # login page
    path('register/', register_view, name='register'), # register page 
    path('logout/', logout_view, name='logout'), # logout 
    path('exam/<pk>', exam_view, name='exam'), # exam detail 
    path('result/<pk>', result_view, name='result'), # result detail 
    path('monitor/', monitor_list_view, name='monitor'), # monitor page 
    path('monitor/<pk>', monitor_detail_view, name='monitor-detail'), # monitor detail 
    path('monitoring/upload_video/<pk>', upload_video, name='upload-video'), # api upload video 
    path('api/check_cheating_status/<int:pk>/', check_done_status, name='check_done_status'), # api check status
    path('result-list', result_list_view, name='result-list'),
    path('ranking/<pk>', ranking_detail_view, name='ranking'),
    path('ranking-list', ranking_list_view, name='ranking-list'),
]
