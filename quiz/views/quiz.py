from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required 
from django.http import Http404, HttpResponse, JsonResponse 
from quiz.models.quiz import *


@login_required(login_url='/login/')
def exam_view(request, pk):
    context = dict()
    try:
        exam = Exam.objects.get(pk=pk)
        counter = exam.total_questions
        part1_questions = exam.part_1.all()
        part2_questions = exam.part_2.all()
        part3_questions = exam.part_3.all()
        context['exam'] = exam 
        context['counter'] = counter 
        context['part1_questions'] = part1_questions 
        context['part2_questions'] = part2_questions 
        context['part3_questions'] = part3_questions 

    except Exam.DoesNotExist:
        return HttpResponse('<h1>404 Not Found</h1>', status=404)
    
    # check số lượt thi 
    user = request.user 
    if Result.objects.filter(exam=exam, user=user).exists():
        if Result.objects.filter(exam=exam, user=user).count() >= exam.retry:
            return render(request, 'quiz/done.html', status=200)
        for r in Result.objects.filter(exam=exam, user=user):
            r.is_on_rank = False
            r.save()
    
    # nộp bài
    if request.method == 'POST':
        print(request.POST)
        elapsed_time = request.POST.get('elapsed_time')
        try:
            print(elapsed_time)
            if isinstance(elapsed_time, list):
                elapsed_time = int(elapsed_time[0])
            else:
                elapsed_time = int(elapsed_time)
        except Exception as e:
            elapsed_time = 0
        score = 0
        result = Result.objects.create(
            exam=exam,
            user=request.user,
            score=score,
            exam_time=elapsed_time,
            is_on_rank=True,
        )

        # xử lý câu hỏi lựa chọn đáp án
        for q in exam.part_1.all():
            selected_answer_id = request.POST.get(f'question_{q.id}')
            if selected_answer_id and selected_answer_id != "":
                selected_answer = int(selected_answer_id)
                ResultDetail.objects.create(
                    result=result,
                    question=q,
                    answer=selected_answer,
                    correct_answer=q.correct,
                    is_correct=selected_answer == q.correct,
                )
                if selected_answer == q.correct:
                    score += 1
            else:
                ResultDetail.objects.create(
                    result=result,
                    question=q,
                    answer=None,  
                    correct_answer=q.correct,
                    is_correct=False, 
                )


        # Xử lý câu hỏi đúng sai với các mệnh đề
        for q in exam.part_2.all():
            count_temp = 0
            for a in q.answertruefalse_set.all():
                user_answer = request.POST.get(f'question_tf_{q.id}_{a.id}')
                if user_answer:
                    is_correct = (user_answer == a.answer)  # Kiểm tra đáp án người dùng với đáp án đúng của câu trả lời
                    ResultTrueFalse.objects.create(
                        result=result,
                        question=q,
                        answer=user_answer,
                        correct_answer=a.answer,
                        is_correct=is_correct,
                        clause=a.clause,
                    )
                    if is_correct:
                        # score += 10  # Cộng điểm nếu đáp án đúng
                        count_temp += 1 
                else:
                    ResultTrueFalse.objects.create(
                        result=result,
                        question=q,
                        answer='',
                        correct_answer=a.answer,
                        is_correct=False,
                        clause=a.clause,
                    )
            if count_temp == 1:
                score += 0.1
            elif count_temp == 2:
                score += 0.25
            elif count_temp == 3:
                score += 0.5
            elif count_temp == 4: 
                score += 1

        
        # Xử lý câu hỏi điền đáp án
        for q in exam.part_3.all():
            user_answer = request.POST.get(f'question_fill_{q.id}')
            is_correct = user_answer.strip().lower() == q.answer.strip().lower()  # So sánh không phân biệt hoa thường
            ResultFill.objects.create(
                result=result,
                question=q,
                answer=user_answer,
                correct_answer=q.answer,
                is_correct=is_correct
            )
            if is_correct:
                score += 1  # Điểm cho câu hỏi điền đáp án đúng


        result.score = score 
        result.save()
        return redirect('result', pk=result.id)



    return render(request, 'quiz/exam.html', context, status=200)



@login_required(login_url='/login/')
def result_view(request, pk):
    try:
        result = Result.objects.get(pk=pk)
        result_details = ResultDetail.objects.filter(result=result)
        # 1 câu hỏi có 4 mệnh đề thì có 4 result 
        tf_data = list()
        for q in result.exam.part_2.all():
            obj = dict()
            obj['q_id'] = q.id 
            obj['q_text'] = q.text 
            obj['q_clause_list'] = list()
            true_false_details = ResultTrueFalse.objects.filter(result=result, question=q)
            for answ in true_false_details:
                temp = dict()
                temp['rd_id'] = answ.id 
                temp['rd_clause'] = answ.clause
                temp['rd_answer'] = answ.answer 
                temp['rd_correct_answer'] = answ.correct_answer 
                temp['is_correct'] = answ.is_correct 
                obj['q_clause_list'].append(temp)
            tf_data.append(obj)


        fill_details = ResultFill.objects.filter(result=result)
    except Result.DoesNotExist:
        raise Http404()

    return render(request, 'quiz/result.html', {
        'result': result,
        'result_details': result_details,
        'tf_data': tf_data,
        'fill_details': fill_details,
    })


def result_list_view(request):
    if request.user.is_authenticated:
        results = Result.objects.filter(user=request.user).order_by('-updated_at')
        return render(request, 'quiz/result-list.html', {'results': results}, status=200)  
    else:
        return HttpResponse('<h1>404 Not Found</h1>', status=404)


@login_required(login_url='/login/')
def check_done_status(request, pk):
    try:
        result = Result.objects.get(pk=pk)
    except Result.DoesNotExist:
        return JsonResponse({
            'flag': False,
            'message': 'Not found',
        }, status=404)
    
    if result.is_done:
        return JsonResponse({
            'is_cheat': result.is_cheat,
            'reason': result.reason,
            'flag': True,
            'message': 'Oke'
        }, status=200)
    else:
        return JsonResponse({
            'flag': False,
            'message': 'Not Found'
        })
    

def ranking_detail_view(request, pk):
    try:
        exam = Exam.objects.get(pk=pk)
    except Exception as e:
        return HttpResponse('<h1>404 Not Found</h1>', status=404)
    
    results = Result.objects.filter(exam=exam, is_on_rank=True).order_by('score').order_by('exam_time')
    return render(request, 'quiz/ranking.html', {'results': results}, status=200)


def ranking_list_view(request):
    rank_list = Exam.objects.order_by('-updated_at')
    # if request.user.is_authenticated:
    #     if request.user.has_perm('change_teacherprofile') and request.user.teacherprofile:
    #         rank_list = Exam.objects.filter(created_by=request.user.teacherprofile).order_by('-updated_at')
    #     elif request.user.has_perm('view_studentprofile') and request.user.studentprofile and request.user.studentprofile.classroom:
    #         rank_list = Exam.objects.filter(classroom=request.user.studentprofile.classroom)
    return render(request, 'quiz/ranking-list.html', {'rank_list': rank_list}, status=200)

