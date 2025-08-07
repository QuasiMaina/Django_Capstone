from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Choice, GameSession, ChoiceLog
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string

def home(request):
    return render(request, 'play/home.html')

def about(request):
    return render(request, 'play/about.html')

def instructions(request):
    return render(request, 'play/instructions.html')

def question(request):
    return render(request, 'play/question.html')  

@login_required
def start_game(request):
    first_question = Question.objects.first()
    if not first_question:
        return render(request, 'game/no_questions.html')

    session = GameSession.objects.create(
        user=request.user,
        session_id=get_random_string(12),
        current_node=first_question
    )
    return redirect('get_question', session_id=session.session_id)

@login_required
def get_question(request, session_id):
    session = get_object_or_404(GameSession, session_id=session_id, user=request.user)

    if session.completed:
        return redirect('get_result', session_id=session.session_id)

    question = session.current_node
    if not question:
        return render(request, 'play/no_question.html')

    context = {
        'session_id': session.session_id,
        'question': question,
        'choices': question.choices_for_question.all()
    }
    return render(request, 'play/question.html', context)

@login_required
def submit_choice(request, session_id):
    session = get_object_or_404(GameSession, session_id=session_id, user=request.user)

    if session.completed:
        return redirect('get_result', session_id=session_id)

    if request.method == 'POST':
        choice_id = request.POST.get('choice_id')
        score = int(request.POST.get('score', 1))

        if not choice_id:
            return render(request, 'play/question.html', {
                'error': 'Please select a choice.',
                'session_id': session.session_id,
                'question': session.current_node,
                'choices': session.current_node.choices_for_question.all()
            })

        choice = get_object_or_404(Choice, id=choice_id)

        ChoiceLog.objects.create(
            session=session,
            question=choice.question,
            choice=choice,
            score_given=score
        )

        if choice.next_question:
            session.current_node = choice.next_question
        else:
            session.current_node = None
            session.completed = True

        session.save()

        return redirect('get_question', session_id=session_id)

    return redirect('get_question', session_id=session_id)

@login_required
def get_result(request, session_id):
    session = get_object_or_404(GameSession, session_id=session_id, user=request.user)

    if not session.completed:
        return redirect('get_question', session_id=session_id)

    logs = ChoiceLog.objects.filter(session=session)
    total_score = sum(log.score_given for log in logs)

    if total_score < 3:
        diagnosis = "Mild Anxiety Indicators"
    elif 3 <= total_score < 6:
        diagnosis = "Moderate Anxiety Tendencies"
    else:
        diagnosis = "High Anxiety Symptoms"

    session.result = diagnosis
    session.save()

    context = {
        'result': diagnosis,
        'score': total_score,
        'logs': logs,
        'session_id': session_id
    }
    return render(request, 'play/result.html', context)

@login_required
def clear_session(request, session_id):
    session = get_object_or_404(GameSession, session_id=session_id, user=request.user)
    ChoiceLog.objects.filter(session=session).delete()
    session.delete()
    return redirect('start_game')
