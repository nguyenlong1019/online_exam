from django.contrib import admin
from quiz.models.quiz import * 
from .utils import to_blank_window, to_display_image 
from django.urls import reverse


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    search_fields = ['id', 'fullname']
    list_display = ['id', 'display_img', 'fullname', 'position']
    list_filter = ['created_at', 'updated_at', 'gender']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at', 'updated_at']


    fieldsets = (
        ('Chỉnh sửa thông tin', {
            'fields': (
                'id', 'created_at', 'avt',
                'fullname', 'position', 'dob', 'gender', 'address',
                'phone', 'user', 'updated_at'
            )
        }),
    )


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs 
        return qs.filter(user=request.user)


    @admin.display(description='Ảnh')
    def display_img(self, obj):
        if obj.id and obj.avt and obj.avt.url:
            return to_display_image(f"{obj.avt.url}", 'Avatar')
        else:
            return to_display_image('', '')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    search_fields = ['id', 'fullname']
    list_display = ['id', 'display_img', 'fullname', 'classroom']
    list_filter = ['created_at', 'updated_at', 'gender']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at', 'updated_at']

    @admin.display(description='Ảnh')
    def display_img(self, obj):
        if obj.id and obj.avt and obj.avt.url:
            return to_display_image(f"{obj.avt.url}", 'Avatar')
        else:
            return to_display_image('', '')


    fieldsets = (
        ('Chỉnh sửa thông tin', {
            'fields': (
                'id', 'created_at', 'avt',
                'fullname', 'classroom', 'dob', 'gender', 'address',
                'phone', 'user', 'updated_at'
            )
        }),
    )


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs 
        elif request.user.is_staff and request.user.has_perm('quiz.add_studentprofile'):
            return qs 
        return qs.filter(user=request.user) 
    

class StudentInlineAdmin(admin.StackedInline):
    model = StudentProfile
    extra = 30

    fieldsets = (
        ('Thông tin', {
            'fields': (
                'id', 'fullname', 'dob', 'gender', 'user'
            )
        }),
    )


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name']
    list_display = ['id', 'name', 'teacher']
    list_filter = ['created_at', 'updated_at', 'academic_year', 'class_size']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at','updated_at'] 
    inlines = [StudentInlineAdmin]


    fieldsets = (
        ('Lớp học', {
            'fields': (
                'id', 'created_at', 'avt',
                'name', 'teacher', 'academic_year', 'class_size', 
                'updated_at'
            )
        }),
    )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name',]
    list_display = ['id', 'name', 'teaching_hour']
    list_filter = ['created_at', 'updated_at', 'teaching_hour']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at','updated_at'] 
    
    fieldsets = (
        ('Môn học', {
            'fields': (
                'id', 'created_at', 'avt',
                'name', 'teaching_hour', 
                'updated_at'
            )
        }),
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['id', 'text']
    list_display = ['id', 'text']
    list_filter = ['created_at', 'updated_at']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at','updated_at']

    fieldsets = (
        ('Câu hỏi (choices)', {
            'fields': (
                'id', 'created_at', 'text',
                'answer1', 'answer2', 'answer3', 'answer4', 'correct', 'updated_at'
            )
        }),
    )


class AnswerTrueFalseInline(admin.StackedInline):
    model = AnswerTrueFalse 
    extra = 4 

    fieldsets = (
        ('', {
            'fields': (
                'clause', 'answer'
            )
        }),
    )


@admin.register(QuestionTrueFalse)
class QuestionTrueFalseAdmin(admin.ModelAdmin):
    search_fields = ['id', 'text']
    list_display = ['id', 'text']
    list_filter = ['created_at', 'updated_at']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at','updated_at']
    inlines = [AnswerTrueFalseInline]

    fieldsets = (
        ('Câu hỏi đúng sai', {
            'fields': (
                'id', 'created_at', 'text', 'updated_at'
            )
        }),
    )


@admin.register(QuestionFill)
class QuestionFillAdmin(admin.ModelAdmin):
    search_fields = ['id', 'text']
    list_display = ['id', 'text']
    list_filter = ['created_at', 'updated_at']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at','updated_at']

    fieldsets = (
        ('', {
            'fields': (
                'id', 'created_at', 'text', 'answer', 'updated_at'
            )
        }),
    )


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    search_fields = ['id', 'title', 'room_name', 'room_code']
    list_display = ['id', 'room_code', 'start_link', 'room_name']
    list_filter = ['created_at', 'updated_at', 'classroom']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at','updated_at']

    fieldsets = (
        ('', {
            'fields': (
                'id', 'created_at', 'thumb', 'classroom', 'subject',
                'room_code', 'room_name', 'title', 'start_time',
                'finish_time', 'time_todo', 'created_by', 'retry',
                'part_1', 'part_2', 'part_3',
                'updated_at'
            )
        }),
    )

    @admin.display(description='Start Exam')
    def start_link(self, obj):
        if obj.id:
            return to_blank_window(f"{reverse('exam', args=[obj.id])}", 'Start')
        else:
            return ''


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    search_fields = ['id', 'score', 'rank', 'exam_time', 'user', 'exam']
    list_display = ['id', 'exam', 'score', 'rank', 'exam_time']
    list_filter = ['created_at', 'updated_at', 'user', 'exam']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at','updated_at'] 

    fieldsets = (
        ('', {
            'fields': (
                'id', 'created_at', 'user', 'exam',
                'score', 'exam_time', 'rank', 'time_char',
                'is_cheat', 'reason', 'is_done', 'is_on_rank',
                'updated_at'
            )
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.has_perm('change_teacherprofile'):
            return qs 
        return qs.filter(user=request.user)


@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    search_fields = ['id', 'exam', 'user', 'room_code']
    list_display = ['id', 'user', 'exam', 'is_cheat']
    list_filter = ['created_at', 'updated_at', 'is_cheat', 'exam', 'user']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at','updated_at']

    fieldsets = (
        ('', {
            'fields': (
                'id', 'created_at', 'user', 'exam',
                'video', 'is_cheat', 'reason',
                'updated_at'
            )
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.has_perm('change_teacherprofile'):
            return qs 
        return qs.filter(user=request.user)
