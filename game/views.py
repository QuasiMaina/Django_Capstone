from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice, GameSession, ChoiceLog, DISORDER_TYPES
from collections import defaultdict

DISORDER_NAMES = dict(DISORDER_TYPES)  # Map short code to full name
DISORDER_KEYS = set(DISORDER_NAMES.keys())  # Set of valid codes

def home(request):
    return render(request, 'play/home.html')

def start_game(request):
    session = GameSession.objects.create()
    return redirect('get_question', session_id=session.session_id)

def get_question(request, session_id):
    session = get_object_or_404(GameSession, session_id=session_id)

    last_log = ChoiceLog.objects.filter(session=session).order_by('-timestamp').first()

    if last_log:
        question = Question.objects.filter(id__gt=last_log.question.id).order_by('id').first()
    else:
        question = Question.objects.order_by('id').first()

    if not question:
        return redirect('get_result', session_id=session_id)

    return render(request, 'play/question.html', {
        'session_id': session_id,
        'question': question,
        'choices': question.choices.all()
    })

def submit_choice(request, session_id):
    if request.method == 'POST':
        session = get_object_or_404(GameSession, session_id=session_id)
        question_id = request.POST.get('question_id')
        choice_id = request.POST.get('choice')

        question = get_object_or_404(Question, id=question_id)
        choice = get_object_or_404(Choice, id=choice_id)

        # Make sure disorder_type is one of the short codes
        disorder_code = choice.disorder_type if choice.disorder_type in DISORDER_KEYS else None

        ChoiceLog.objects.create(
            session=session,
            question=question,
            choice=choice,
            disorder_type=disorder_code,
            score_given=choice.score
        )

        next_question = Question.objects.filter(id__gt=question.id).order_by('id').first()
        if next_question:
            return redirect('get_question', session_id=session_id)
        else:
            return redirect('get_result', session_id=session_id)

    return redirect('get_question', session_id=session_id)

def get_result(request, session_id):
    session = get_object_or_404(GameSession, session_id=session_id)
    logs = ChoiceLog.objects.filter(session=session)

    score_summary = defaultdict(int)
    for log in logs:
        if log.disorder_type:
            score_summary[log.disorder_type] += log.score_given

    result = None
    if score_summary:
        result = max(score_summary.items(), key=lambda x: x[1])

    # Convert codes to full names for template
    readable_scores = {DISORDER_NAMES.get(k, k): v for k, v in score_summary.items()}
    readable_diagnosis = (DISORDER_NAMES.get(result[0]), result[1]) if result else None

    return render(request, 'play/result.html', {
        'session_id': session_id,
        'score_summary': readable_scores,
        'diagnosis': readable_diagnosis
    })
