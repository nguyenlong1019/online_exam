from django.urls import path 
from quiz.views.index import * 
from quiz.views.quiz import * 
from quiz.views.monitor import * 


urlpatterns = [
    path('', index_view, name='index'),
    path('login/', login_view, name='login'),
    # path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('exam/<pk>', exam_view, name='exam'),
    path('result/<pk>', result_view, name='result'),
    path('monitor/', monitor_list_view, name='monitor'),
    path('monitor/<pk>', monitor_detail_view, name='monitor-detail'),
    path('monitoring/upload_video/<pk>', upload_video, name='upload-video'),
    path('api/check_cheating_status/<int:pk>/', check_done_status, name='check_done_status'),

]
