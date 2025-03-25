from django.db import models 
from django.contrib.auth.models import User 
from django.utils import timezone 
from django.dispatch import receiver 
from django.db.models.signals import post_save 
import os 
import subprocess 
from ckeditor_uploader.fields import RichTextUploadingField


class CommonAbstract(models.Model):
    created_at = models.DateTimeField(editable=False, null=True, blank=True, verbose_name='Thời điểm tạo')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Thời điểm cập nhật')


    class Meta:
        ordering = ('-created_at',)
        abstract = True 


    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        super(CommonAbstract, self).save(*args, **kwargs)


GENDER = (
    (0, 'Nữ'),
    (1, 'Nam')
)


class Subject(CommonAbstract):
    id = models.SmallAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=255, verbose_name='Tên môn học')
    teaching_hour = models.SmallIntegerField(default=18, verbose_name='Số tiết giảng dạy')


    class Meta:
        verbose_name = 'Môn học'
        verbose_name_plural = 'Môn học'
        db_table = 'subjects'


    def __str__(self):
        return f"{self.name} - {self.teaching_hour} Tiết"


class TeacherProfile(CommonAbstract):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
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


    def __str__(self):
        return self.fullname if self.fullname else str(self.id) 


class Classroom(CommonAbstract):
    id = models.SmallAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=255, verbose_name='Tên lớp')
    teacher = models.OneToOneField(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Giáo viên chủ nhiệm')
    academic_year = models.CharField(max_length=25, null=True, blank=True, verbose_name='Năm học')
    class_size = models.SmallIntegerField(default=30, verbose_name='Sĩ số')


    class Meta:
        verbose_name = 'Lớp học'
        verbose_name_plural = 'Lớp học'
        db_table = 'classroom'


    def __str__(self):
        return f"{self.name} - GV: {self.teacher.fullname}" if self.name and self.teacher else f"{self.id}"


class StudentProfile(CommonAbstract):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
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


    def __str__(self):
        return self.fullname if self.fullname else str(self.id)


class Exam(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=255, verbose_name='Tên bài kiểm tra')
    room_name = models.CharField(max_length=255, verbose_name='Tên phòng thi')
    start_time = models.DateTimeField(verbose_name='Thời gian bắt đầu')
    finish_time = models.DateTimeField(verbose_name='Thời gian kết thúc')
    time_todo = models.IntegerField(default=15, verbose_name='Thời gian làm bài (phút)')
    room_code = models.CharField(max_length=15, unique=True, verbose_name='Mã phòng thi')
    created_by = models.CharField(max_length=255, verbose_name='Người tạo')
    retry = models.SmallIntegerField(default=1, verbose_name='Số lượt thi tối đa')
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, verbose_name='Lớp')


    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Bài kiểm tra'
        verbose_name_plural = 'Bài kiểm tra'
        db_table = 'exams'


    def __str__(self):
        return f"{self.id} - {self.title} - {self.room_code}"
    

class MathExam(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=255, verbose_name='Tên bài kiểm tra')
    room_name = models.CharField(max_length=255, verbose_name='Tên phòng thi')
    start_time = models.DateTimeField(verbose_name='Thời gian bắt đầu')
    finish_time = models.DateTimeField(verbose_name='Thời gian kết thúc')
    time_todo = models.IntegerField(default=15, verbose_name='Thời gian làm bài (phút)')
    room_code = models.CharField(max_length=15, unique=True, verbose_name='Mã phòng thi')
    created_by = models.CharField(max_length=255, verbose_name='Người tạo')
    retry = models.SmallIntegerField(default=1, verbose_name='Số lượt thi tối đa')
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, verbose_name='Lớp')


    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Kiểm tra toán'
        verbose_name_plural = 'Kiểm tra toán'
        db_table = 'math_exams'


    def __str__(self):
        return f"{self.id} - {self.title} - {self.room_code}"


class MathQuestion(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    exam = models.ForeignKey(MathExam, on_delete=models.CASCADE, verbose_name='Bài kiểm tra')
    question_text = RichTextUploadingField(null=True, blank=True, verbose_name='Câu hỏi')


    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Câu hỏi toán'
        verbose_name_plural = 'Câu hỏi toán'
        db_table = 'math_questions'


    def __str__(self):
        return f"{self.id} - {self.question_text}"
    

class Question(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name='Bài kiểm tra')
    question_text = models.CharField(max_length=255, verbose_name='Câu hỏi')


    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Câu hỏi'
        verbose_name_plural = 'Câu hỏi'
        db_table = 'questions'


    def __str__(self):
        return f"{self.id} - {self.question_text}"


class MathAnswer(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    question = models.ForeignKey(MathQuestion, on_delete=models.CASCADE, verbose_name='Câu hỏi')
    answer_text = RichTextUploadingField(null=True, blank=True, verbose_name='Câu trả lời')
    is_correct = models.BooleanField(default=False, verbose_name='Câu trả lời đúng')


    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Đáp án toán'
        verbose_name_plural = 'Đáp án toán'
        db_table = 'math_answers'

    
    def __str__(self):
        return f"{self.id} - {self.answer_text}"
    

class Answer(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Câu hỏi')
    answer_text = models.CharField(max_length=255, verbose_name='Câu trả lời')
    is_correct = models.BooleanField(default=False, verbose_name='Câu trả lời đúng')


    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Đáp án'
        verbose_name_plural = 'Đáp án'
        db_table = 'answers'

    
    def __str__(self):
        return f"{self.id} - {self.answer_text}"


class MathQuestionTrueFalse(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    exam = models.ForeignKey(MathExam, on_delete=models.CASCADE, verbose_name='Bài kiểm tra', null=True)
    question_text = RichTextUploadingField(null=True, blank=True, verbose_name='Câu hỏi')

    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Toán đúng sai '
        verbose_name_plural = 'Toán đúng sai'
        db_table = 'math_question_tf'

    
    def __str__(self):
        return f"{self.id} - {self.question_text}"
    

class QuestionTrueFalse(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name='Bài kiểm tra', null=True)
    question_text = models.CharField(max_length=255, verbose_name='Câu hỏi')

    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Câu hỏi đúng sai'
        verbose_name_plural = 'Câu hỏi đúng sai'
        db_table = 'question_tf'

    
    def __str__(self):
        return f"{self.id} - {self.question_text}"


class MathAnswerTrueFalse(CommonAbstract):
    TF = (
        ('true', 'true'),
        ('false', 'false'),
    )

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    question = models.ForeignKey(MathQuestionTrueFalse, on_delete=models.SET_NULL, null=True, verbose_name='Câu hỏi')
    clause = RichTextUploadingField(null=True, blank=True, verbose_name='Mệnh đề')
    answer = models.CharField(max_length=7, default='true', choices=TF, verbose_name='Đáp án')


    class Meta:
        verbose_name = 'Đáp án Toán đúng sai'
        verbose_name_plural = 'Đáp án Toán đúng sai'
        db_table = 'math_answer_tf'


    def __str__(self):
        return f"{self.id}"


class AnswerTrueFalse(CommonAbstract):
    TF = (
        ('true', 'true'),
        ('false', 'false'),
    )

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    question = models.ForeignKey(QuestionTrueFalse, on_delete=models.SET_NULL, null=True, verbose_name='Câu hỏi')
    clause = models.CharField(max_length=255, verbose_name='Mệnh đề')
    answer = models.CharField(max_length=7, default='true', choices=TF, verbose_name='Đáp án')


    class Meta:
        verbose_name = 'Đáp án đúng sai'
        verbose_name_plural = 'Đáp án đúng sai'
        db_table = 'answer_tf'


    def __str__(self):
        return f"{self.id}"
    

class MathQuestionFill(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    exam = models.ForeignKey(MathExam, on_delete=models.CASCADE, verbose_name='Bài kiểm tra', null=True)
    question_text = RichTextUploadingField(null=True, blank=True, verbose_name='Câu hỏi')
    answer = RichTextUploadingField(null=True, blank=True, verbose_name='Đáp án đúng')


    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Câu hỏi điền đáp án (Toán)'
        verbose_name_plural = 'Câu hỏi điền đáp án (Toán)'
        db_table = 'math_question_fill'
    

    def __str__(self):
        return f"{self.id} - {self.question_text} - {self.answer}"


class QuestionFill(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name='Bài kiểm tra', null=True)
    question_text = models.CharField(max_length=255, null=True, blank=True, verbose_name='Câu hỏi')
    answer = models.CharField(max_length=255, null=True, blank=True, verbose_name='Đáp án đúng')


    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Câu hỏi điền đáp án'
        verbose_name_plural = 'Câu hỏi điền đáp án'
        db_table = 'question_fill'
    

    def __str__(self):
        return f"{self.id} - {self.question_text} - {self.answer}"


class Result(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Người thực hiện')
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, verbose_name='Bài thi')
    score = models.IntegerField(default=0, verbose_name='Điểm số')
    is_cheat = models.BooleanField(default=False, verbose_name='Trạng thái gian lận')
    is_done = models.BooleanField(default=False, verbose_name='Kiểm tra gian lận hoàn thành')
    reason = models.CharField(max_length=255, default='', verbose_name='Lý do phát hiện gian lận')
    

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Kết quả thi'
        verbose_name_plural = 'Kết quả thi'
        db_table = 'results'

    
    def __str__(self):
        return f"{self.id} - {self.user.username}"
    

class MathResult(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Người thực hiện')
    exam = models.ForeignKey(MathExam, on_delete=models.SET_NULL, null=True, verbose_name='Bài thi')
    score = models.IntegerField(default=0, verbose_name='Điểm số')
    is_cheat = models.BooleanField(default=False, verbose_name='Trạng thái gian lận')
    is_done = models.BooleanField(default=False, verbose_name='Kiểm tra gian lận hoàn thành')
    reason = models.CharField(max_length=255, default='', verbose_name='Lý do phát hiện gian lận')
    

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Kết quả thi (Toán)'
        verbose_name_plural = 'Kết quả thi (Toán)'
        db_table = 'math_results'

    
    def __str__(self):
        return f"{self.id} - {self.user.username}"
    

class ResultDetail(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    result = models.ForeignKey(Result, on_delete=models.CASCADE, verbose_name='Bài kiểm tra')
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, verbose_name='Câu hỏi')
    answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True, verbose_name='Đáp án lựa chọn')
    is_correct = models.BooleanField(default=False, verbose_name='Kết quả (Đ/S)')


    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Kết quả câu hỏi'
        verbose_name_plural = 'Kết quả câu hỏi'
        db_table = 'result_details'

    
    def __str__(self):
        return f"{self.id} - {self.is_correct}"
    

    def save(self, *args, **kwargs):
        if self.answer and self.answer.is_correct:
            self.is_correct = True 
        super(ResultDetail, self).save(*args, **kwargs)


class MathResultDetail(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    result = models.ForeignKey(MathResult, on_delete=models.CASCADE, verbose_name='Bài kiểm tra')
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, verbose_name='Câu hỏi')
    answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True, verbose_name='Đáp án lựa chọn')
    is_correct = models.BooleanField(default=False, verbose_name='Kết quả (Đ/S)')


    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Kết quả câu hỏi (Toán)'
        verbose_name_plural = 'Kết quả câu hỏi (Toán)'
        db_table = 'math_result_details'

    
    def __str__(self):
        return f"{self.id} - {self.is_correct}"
    

    def save(self, *args, **kwargs):
        if self.answer and self.answer.is_correct:
            self.is_correct = True 
        super(ResultDetail, self).save(*args, **kwargs)



class ResultDetail(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    result = models.ForeignKey(Result, on_delete=models.CASCADE, verbose_name='Bài kiểm tra')
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, verbose_name='Câu hỏi')
    answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True, verbose_name='Đáp án lựa chọn')
    is_correct = models.BooleanField(default=False, verbose_name='Kết quả (Đ/S)')


    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Kết quả câu hỏi'
        verbose_name_plural = 'Kết quả câu hỏi'
        db_table = 'result_details'

    
    def __str__(self):
        return f"{self.id} - {self.is_correct}"
    

    def save(self, *args, **kwargs):
        if self.answer and self.answer.is_correct:
            self.is_correct = True 
        super(ResultDetail, self).save(*args, **kwargs)

    
class ResultTrueFalse(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    result = models.ForeignKey(Result, on_delete=models.CASCADE, verbose_name='Bài kiểm tra', null=True)
    question = models.ForeignKey(QuestionTrueFalse, on_delete=models.SET_NULL, null=True, verbose_name='Câu hỏi')
    answer = models.CharField(max_length=7, verbose_name='Đáp án chọn', default='')
    is_correct = models.BooleanField(default=False, verbose_name='Kết quả (Đ/S)')

    
    class Meta:
        verbose_name = 'Kết quả đúng sai'
        verbose_name_plural = 'Kết quả đúng sai'
        db_table = 'result_tf'

    
    def __str__(self):
        return f"{self.id}"


class ResultFill(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    result = models.ForeignKey(Result, on_delete=models.CASCADE, verbose_name='Bài kiểm tra', null=True)
    question = models.ForeignKey(QuestionFill, on_delete=models.SET_NULL, null=True, verbose_name='Câu hỏi')
    answer = RichTextUploadingField(null=True, blank=True, verbose_name='Câu trả lời')
    is_correct = models.BooleanField(default=False, verbose_name='Kết quả (Đ/S)')


    class Meta:
        verbose_name = 'Kết quả điền'
        verbose_name_plural = 'Kết quả điền'
        db_table = 'result_fill'

    
    def __str__(self):
        return f"{self.id}"


class Monitor(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # result = models.ForeignKey(Result, on_delete=models.SET_NULL, null=True, verbose_name='Kết quả')
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


class MathMonitor(CommonAbstract):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    exam = models.ForeignKey(MathExam, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # result = models.ForeignKey(Result, on_delete=models.SET_NULL, null=True, verbose_name='Kết quả')
    video = models.FileField(null=True, blank=True, upload_to='video/')
    is_cheat = models.BooleanField(default=False, verbose_name='Trạng thái gian lận')
    reason = models.CharField(max_length=255, default='', verbose_name='Lý do phát hiện gian lận')


    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Video giám sát (Math)'
        verbose_name_plural = 'Video giám sát (Math)'
        db_table = 'math_monitors'

    
    def __str__(self):
        return f"{self.id} - {self.created_at} - {self.is_cheat}"
