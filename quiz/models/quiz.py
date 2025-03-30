from django.db import models 
from django.contrib.auth.models import User 
from django.utils import timezone 
from django.dispatch import receiver 
from django.db.models.signals import post_save 
import os 
import subprocess 
from ckeditor_uploader.fields import RichTextUploadingField


class CommonAbstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Thời điểm tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Thời điểm cập nhật')


    class Meta:
        ordering = ('-created_at',)
        abstract = True 


GENDER = (
    (0, 'Nữ'),
    (1, 'Nam')
)


class Subject(CommonAbstract):
    id = models.SmallAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    avt = models.ImageField(upload_to='subject_imgs/', null=True, blank=True, verbose_name='Ảnh đại diện')
    name = models.CharField(max_length=255, verbose_name='Tên môn học')
    teaching_hour = models.SmallIntegerField(default=18, verbose_name='Số tiết giảng dạy')


    class Meta:
        verbose_name = 'Môn học'
        verbose_name_plural = 'Môn học'
        db_table = 'subjects'
        ordering = ['-updated_at', 'name', '-teaching_hour']


    def __str__(self):
        return f"{self.name} - {self.teaching_hour} Tiết"


class TeacherProfile(CommonAbstract):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    avt = models.ImageField(upload_to='teacher_imgs/', null=True, blank=True, verbose_name='Ảnh đại diện')
    fullname = models.CharField(max_length=255, verbose_name='Họ và tên', null=True, blank=True)
    dob = models.DateField(null=True, blank=True, verbose_name='Ngày sinh')
    gender = models.SmallIntegerField(null=True, blank=True, choices=GENDER, verbose_name='Giới tính')
    
    address = models.TextField(null=True, blank=True, verbose_name='Địa chỉ')
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='Số điện thoại')
    position = models.CharField(max_length=255, verbose_name='Vị trí giảng dạy')
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL, verbose_name='Tài khoản')

    class Meta:
        verbose_name = 'Giáo viên'
        verbose_name_plural = 'Giáo viên'
        db_table = 'teacher_profiles'
        ordering = ['-updated_at', 'fullname',]


    def __str__(self):
        return self.fullname if self.fullname else str(self.id) 


class Classroom(CommonAbstract):
    id = models.SmallAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    avt = models.ImageField(upload_to='classroom_imgs/', null=True, blank=True, verbose_name='Ảnh đại diện')
    name = models.CharField(max_length=255, verbose_name='Tên lớp')
    teacher = models.OneToOneField(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Giáo viên chủ nhiệm')
    academic_year = models.CharField(max_length=25, null=True, blank=True, verbose_name='Năm học')
    class_size = models.SmallIntegerField(default=30, verbose_name='Sĩ số')


    class Meta:
        verbose_name = 'Lớp học'
        verbose_name_plural = 'Lớp học'
        db_table = 'classroom'
        ordering = ['-updated_at', 'name']


    def __str__(self):
        return f"{self.name} - GV: {self.teacher.fullname}" if self.name and self.teacher else f"{self.id}"


class StudentProfile(CommonAbstract):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    avt = models.ImageField(upload_to='student_imgs/', null=True, blank=True, verbose_name='Ảnh đại diện')
    fullname = models.CharField(max_length=255, verbose_name='Họ và tên', null=True, blank=True)
    dob = models.DateField(null=True, blank=True, verbose_name='Ngày sinh')
    gender = models.SmallIntegerField(null=True, blank=True, choices=GENDER, verbose_name='Giới tính')
    classroom = models.ForeignKey(Classroom, null=True, on_delete=models.SET_NULL, verbose_name='Lớp')
    address = models.TextField(null=True, blank=True, verbose_name='Địa chỉ')
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='Số điện thoại')
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL, verbose_name='Tài khoản')

    class Meta:
        verbose_name = 'Học sinh'
        verbose_name_plural = 'Học sinh'
        db_table = 'student_profiles'
        ordering = ['-updated_at', 'fullname']


    def __str__(self):
        return self.fullname if self.fullname else str(self.id)
    

class Question(CommonAbstract):
    CORRECT_CHOICES = (
        (1, 'A'),
        (2, 'B'),
        (3, 'C'),
        (4, 'D')
    )

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    text = RichTextUploadingField(null=True, blank=True, verbose_name='Câu hỏi')
    answer1 = RichTextUploadingField(null=True, blank=True, verbose_name='A')
    answer2 = RichTextUploadingField(null=True, blank=True, verbose_name='B')
    answer3 = RichTextUploadingField(null=True, blank=True, verbose_name='C')
    answer4 = RichTextUploadingField(null=True, blank=True, verbose_name='D')
    correct = models.SmallIntegerField(default=1, choices=CORRECT_CHOICES, verbose_name='Đáp án đúng')

    class Meta:
        db_table = 'choice_questions'
        verbose_name = 'Câu hỏi'
        verbose_name_plural = 'Câu hỏi'
        ordering = ['-updated_at','text']

    def __str__(self):
        return f"{self.text}" if self.text else f"{self.id}"


class QuestionTrueFalse(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    text = RichTextUploadingField(null=True, blank=True, verbose_name='Câu hỏi')

    class Meta:
        verbose_name = 'Câu hỏi (Đ/S)'
        verbose_name_plural = 'Câu hỏi (Đ/S)'
        db_table = 'tf_questions'
        ordering = ['-updated_at', 'text']

    def __str__(self):
        return f"{self.text}" if self.text else f"{self.id}"


class AnswerTrueFalse(CommonAbstract):
    TF = (
        ('true', 'true'),
        ('false', 'false')
    )
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    question = models.ForeignKey(QuestionTrueFalse, on_delete=models.SET_NULL, null=True, verbose_name='Câu hỏi')
    clause = RichTextUploadingField(null=True, blank=True, verbose_name='Mệnh đề')
    answer = models.CharField(max_length=7, default='false', choices=TF, verbose_name='Đáp án')

    class Meta:
        verbose_name = 'Đáp án (Đ/S)'
        verbose_name_plural = 'Đáp án (Đ/S)'
        db_table = 'tf_answers'
        ordering = ['-updated_at', 'clause']

    def __str__(self):
        return f"{self.clause}" if self.clause else f"{self.id}"


class QuestionFill(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    text = RichTextUploadingField(null=True, blank=True, verbose_name='Câu hỏi')
    answer = models.TextField(null=True, blank=True, verbose_name='Đáp án')

    class Meta:
        verbose_name = 'Câu hỏi điền'
        verbose_name_plural = 'Câu hỏi điền'
        db_table = 'fill_questions'
        ordering = ['-updated_at', 'text']
    
    def __str__(self):
        return f"{self.text}" if self.text else f"{self.id}"


class Exam(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    thumb = models.ImageField(upload_to='exam_imgs/', null=True, blank=True, verbose_name='Ảnh thumbnail')
    title = models.CharField(max_length=255, verbose_name='Tên bài kiểm tra')
    room_name = models.CharField(max_length=255, verbose_name='Tên phòng thi')
    room_code = models.CharField(max_length=15, unique=True, verbose_name='Mã phòng thi')
    start_time = models.DateTimeField(verbose_name='Thời gian bắt đầu')
    finish_time = models.DateTimeField(verbose_name='Thời gian kết thúc')
    time_todo = models.IntegerField(default=15, verbose_name='Thời gian làm bài (phút)')
    retry = models.SmallIntegerField(default=1, verbose_name='Số lượt thi tối đa')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, verbose_name='Môn học')
    created_by = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, verbose_name='Người tạo')
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, verbose_name='Lớp')

    # type = None 

    part_1 = models.ManyToManyField(Question, verbose_name='Phần I')
    part_2 = models.ManyToManyField(QuestionTrueFalse, verbose_name='Phần II')
    part_3 = models.ManyToManyField(QuestionFill, verbose_name='Phần III')


    @property
    def total_questions(self):
        return self.part_1.count() + self.part_2.count() + self.part_3.count()


    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Bài kiểm tra'
        verbose_name_plural = 'Bài kiểm tra'
        db_table = 'exams'


    def __str__(self):
        return f"{self.title} - {self.room_code}" if self.title and self.room_code else f"{self.id}"


class Result(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Người thực hiện')
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, verbose_name='Bài thi')
    score = models.FloatField(default=0, verbose_name='Điểm số')
    rank = models.SmallIntegerField(default=9999, verbose_name='Thứ hạng')
    exam_time = models.IntegerField(default=1, verbose_name='Thời gian thực hiện')
    time_char = models.CharField(max_length=25, null=True, blank=True, verbose_name='Thời gian làm (phút)')
    is_cheat = models.BooleanField(default=False, verbose_name='Trạng thái gian lận')
    is_done = models.BooleanField(default=False, verbose_name='Kiểm tra gian lận hoàn thành')
    reason = models.CharField(max_length=255, default='', verbose_name='Lý do phát hiện gian lận')
    is_on_rank = models.BooleanField(default=False, verbose_name='Được xếp hạng')

    class Meta:
        ordering = ('-updated_at',)
        verbose_name = 'Kết quả thi'
        verbose_name_plural = 'Kết quả thi'
        db_table = 'results'

    
    def __str__(self):
        return f"{self.id} - {self.user.username}"
    

class ResultDetail(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    result = models.ForeignKey(Result, on_delete=models.SET_NULL, null=True, verbose_name='Kết quả thi')
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, verbose_name='Câu hỏi')
    answer = models.SmallIntegerField(null=True, blank=True, verbose_name='Câu trả lời')
    correct_answer = models.SmallIntegerField(null=True, blank=True, verbose_name='Đáp án đúng')
    is_correct = models.BooleanField(null=True, blank=True, verbose_name='Đúng/Sai')


    class Meta:
        ordering = ['-created_at',]
        verbose_name = 'Kết quả phần I'
        verbose_name_plural = 'Kết quả phần I'
        db_table = 'result_details'

    def __str__(self):
        return f"{self.id}" if not self.answer else f"{self.answer}"

    
class ResultTrueFalse(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    result = models.ForeignKey(Result, on_delete=models.CASCADE, verbose_name='Bài kiểm tra', null=True)
    question = models.ForeignKey(QuestionTrueFalse, on_delete=models.SET_NULL, null=True, verbose_name='Câu hỏi')
    answer = models.CharField(max_length=7, verbose_name='Đáp án chọn', default='')
    correct_answer = models.CharField(max_length=7, verbose_name='Đáp án đúng', null=True, blank=True)
    is_correct = models.BooleanField(null=True, blank=True, verbose_name='Đúng/Sai')
    clause = RichTextUploadingField(null=True, blank=True, verbose_name='Mệnh đề')

    
    class Meta:
        ordering = ['-created_at',]
        verbose_name = 'Kết quả phần II'
        verbose_name_plural = 'Kết quả phần II'
        db_table = 'result_tf_details'

    
    def __str__(self):
        return f"{self.id}"


class ResultFill(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    result = models.ForeignKey(Result, on_delete=models.CASCADE, verbose_name='Bài kiểm tra', null=True)
    question = models.ForeignKey(QuestionFill, on_delete=models.SET_NULL, null=True, verbose_name='Câu hỏi')
    answer = models.TextField(null=True, blank=True, verbose_name='Câu trả lời')
    correct_answer = models.TextField(null=True, blank=True, verbose_name='Đáp án đúng')
    is_correct = models.BooleanField(null=True, blank=True, verbose_name='Đúng/Sai')


    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Kết quả phần III'
        verbose_name_plural = 'Kết quả phần III'
        db_table = 'result_fill_details'

    
    def __str__(self):
        return f"{self.id}"


class Monitor(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    video = models.FileField(null=True, blank=True, upload_to='video/')
    is_cheat = models.BooleanField(default=False, verbose_name='Trạng thái gian lận')
    reason = models.CharField(max_length=255, default='', verbose_name='Lý do phát hiện gian lận')


    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Video giám sát'
        verbose_name_plural = 'Video giám sát'
        db_table = 'monitors'

    
    def __str__(self):
        return f"{self.id} - {self.created_at} - {self.is_cheat}"


@receiver(post_save, sender=Monitor)
def handle_cheat(sender, instance, created, **kwargs):
    if created:
        subprocess.Popen(['python', 'handle_cheat.py', str(instance.id)])