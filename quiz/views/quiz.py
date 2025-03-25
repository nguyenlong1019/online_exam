from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required 
from django.http import Http404, HttpResponse, JsonResponse 
from quiz.models.quiz import Exam, Question, Answer, Result, ResultDetail, QuestionTrueFalse, QuestionFill, ResultTrueFalse, ResultFill, AnswerTrueFalse
from django.views.decorators.http import require_GET, require_POST 


@login_required(login_url='/login/')
def exam_view(request, pk):
    try:
        exam = Exam.objects.get(pk=pk)
        counter = len(list(exam.question_set.all()))
    except Exam.DoesNotExist:
        return Http404()
    
    user = request.user 
    if Result.objects.filter(exam=exam, user=user).exists():
        if Result.objects.filter(exam=exam, user=user).count() >= exam.retry:
            return render(request, 'quiz/done.html', status=200)
    
    if request.method == 'POST':
        print(request.POST)
        score = 0
        result = Result.objects.create(
            exam=exam,
            user=request.user,
            score=score
        )

        for q in exam.question_set.all():
            selected_answer_id = request.POST.get(f'question_{q.id}')
            if selected_answer_id and selected_answer_id != "":
                selected_answer = Answer.objects.get(id=selected_answer_id)
                result_detail = ResultDetail.objects.create(
                    result=result,
                    question=q,
                    answer=selected_answer,
                    is_correct=selected_answer.is_correct,
                )
                if selected_answer.is_correct:
                    score += 10 
            else:
                ResultDetail.objects.create(
                    result=result,
                    question=q,
                    answer=None,  
                    is_correct=False, 
                )

        # # Xử lý câu hỏi đúng sai
        # for q in exam.questiontruefalse_set.all():
        #     selected_answer = request.POST.get(f'question_tf_{q.id}')
        #     is_correct = selected_answer == q.answer  # So sánh đáp án người dùng chọn với đáp án đúng
        #     ResultTrueFalse.objects.create(
        #         result=result,
        #         question=q,
        #         answer=selected_answer,
        #         is_correct=is_correct
        #     )
        #     if is_correct:
        #         score += 10  # Điểm cho câu hỏi đúng sai


        # Xử lý câu hỏi đúng sai với các mệnh đề
        for q in exam.questiontruefalse_set.all():
            count_temp = 0
            for a in q.answertruefalse_set.all():
                user_answer = request.POST.get(f'question_tf_{q.id}_{a.id}')
                if user_answer:
                    is_correct = (user_answer == a.answer)  # Kiểm tra đáp án người dùng với đáp án đúng của câu trả lời
                    ResultTrueFalse.objects.create(
                        result=result,
                        question=q,
                        answer=user_answer,
                        is_correct=is_correct
                    )
                    if is_correct:
                        # score += 10  # Cộng điểm nếu đáp án đúng
                        count_temp += 1 
            if count_temp == 1:
                score += 1
            elif count_temp == 2:
                score += 2.5 
            elif count_temp == 3:
                score += 5 
            elif count_temp == 4: 
                score += 10

        
        # Xử lý câu hỏi điền đáp án
        for q in exam.questionfill_set.all():
            user_answer = request.POST.get(f'question_fill_{q.id}')
            is_correct = user_answer.strip().lower() == q.answer.strip().lower()  # So sánh không phân biệt hoa thường
            ResultFill.objects.create(
                result=result,
                question=q,
                answer=user_answer,
                is_correct=is_correct
            )
            if is_correct:
                score += 10  # Điểm cho câu hỏi điền đáp án đúng


        result.score = score 
        result.save()
        return redirect('result', pk=result.id)


    return render(request, 'quiz/exam.html', {'exam': exam, 'counter': counter}, status=200)


# @login_required(login_url='/login/')
# def result_view(request, pk):
#     try:
#         result = Result.objects.get(pk=pk)
#     except Result.DoesNotExist:
#         return Http404()

#     return render(request, 'quiz/result.html', {'result': result})



@login_required(login_url='/login/')
def result_view(request, pk):
    try:
        result = Result.objects.get(pk=pk)
        result_details = ResultDetail.objects.filter(result=result)
        true_false_details = ResultTrueFalse.objects.filter(result=result)
        fill_details = ResultFill.objects.filter(result=result)
    except Result.DoesNotExist:
        raise Http404()

    return render(request, 'quiz/result.html', {
        'result': result,
        'result_details': result_details,
        'true_false_details': true_false_details,
        'fill_details': fill_details,
    })


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
    
