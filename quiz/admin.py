from django.contrib import admin
from quiz.models.quiz import * 
from django.contrib.auth.admin import UserAdmin 
import nested_admin 


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    search_fields = ['id', 'fullname']
    list_display = ['id', 'fullname', 'position']
    list_filter = ['created_at', 'updated_at', 'gender']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at', 'updated_at']


    fieldsets = (
        ('Chỉnh sửa thông tin', {
            'fields': (
                'id', 'created_at',
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



@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    search_fields = ['id', 'fullname']
    list_display = ['id', 'fullname', 'classroom']
    list_filter = ['created_at', 'updated_at', 'gender']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at', 'updated_at']


    fieldsets = (
        ('Chỉnh sửa thông tin', {
            'fields': (
                'id', 'created_at',
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
    readonly_fields = ['id', 'created_at', 'updated_at'] 
    inlines = [StudentInlineAdmin]


    fieldsets = (
        ('Chỉnh sửa thông tin', {
            'fields': (
                'id', 'created_at',
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
    readonly_fields = ['id', 'created_at', 'updated_at'] 
    
    fieldsets = (
        ('Chỉnh sửa thông tin', {
            'fields': (
                'id', 'created_at',
                'name', 'teaching_hour', 
                'updated_at'
            )
        }),
    )

# admin.TabularInline


class AnswerAdminInline(nested_admin.NestedTabularInline):
    model = Answer 
    extra = 4


class QuestionAdminInline(nested_admin.NestedTabularInline):
    model = Question 
    extra = 18 
    inlines = [AnswerAdminInline]


class AnswerTrueFalseAdminInline(nested_admin.NestedTabularInline):
    model = AnswerTrueFalse 
    extra = 4


class QuestionTrueFalseAdminInline(nested_admin.NestedStackedInline):
    model = QuestionTrueFalse 
    extra = 4 
    inlines = [AnswerTrueFalseAdminInline]
    


class QuestionFillAdminInline(admin.StackedInline):
    model = QuestionFill 
    extra = 6 


@admin.register(Exam)
class ExamAdmin(nested_admin.NestedModelAdmin):
    search_fields = ['id', 'title', 'room_name', 'room_code']
    list_display = ['id', 'room_code', 'room_name']
    list_filter = ['created_at', 'updated_at', 'classroom']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines = [QuestionAdminInline, QuestionTrueFalseAdminInline]

    fieldsets = (
        ('Chỉnh sửa thông tin', {
            'fields': (
                'id', 'created_at', 'classroom',
                'room_code', 'room_name', 'title', 'start_time',
                'finish_time', 'time_todo', 'created_by', 'retry',
                'updated_at'
            )
        }),
    )
