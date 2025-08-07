from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Question, Choice, GameSession, ChoiceLog
from django.contrib.auth.models import User
import uuid


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_game(request):
    """
    Start a new game session.
    """
    session_id = str(uuid.uuid4())
    first_question = Question.objects.first()

    session = GameSession.objects.create(
        user=request.user,
        session_id=session_id,
        current_node=first_question
    )

    return Response({
        'session_id': session.session_id,
        'question': first_question.text,
        'choices': [
            {'id': choice.id, 'text': choice.text}
            for choice in first_question.choices_for_question.all()
        ]
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_question(request, session_id):
    """
    Get the current question in the game session.
    """
    session = get_object_or_404(GameSession, session_id=session_id, user=request.user)

    if session.completed:
        return Response({'detail': 'Game already completed.'}, status=status.HTTP_400_BAD_REQUEST)

    question = session.current_node
    if not question:
        return Response({'detail': 'No current question.'}, status=status.HTTP_404_NOT_FOUND)

    return Response({
        'question': question.text,
        'choices': [
            {'id': choice.id, 'text': choice.text}
            for choice in question.choices_for_question.all()
        ]
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_choice(request, session_id):
    """
    Submit a choice for the current question.
    """
    session = get_object_or_404(GameSession, session_id=session_id, user=request.user)

    if session.completed:
        return Response({'detail': 'Game already completed.'}, status=status.HTTP_400_BAD_REQUEST)

    choice_id = request.data.get('choice_id')
    score = request.data.get('score', 1)

    if not choice_id:
        return Response({'detail': 'Choice ID required.'}, status=status.HTTP_400_BAD_REQUEST)

    choice = get_object_or_404(Choice, id=choice_id)

    # Record the choice
    ChoiceLog.objects.create(
        session=session,
        question=choice.question,
        choice=choice,
        score_given=score
    )

    # Determine next step
    if choice.next_question:
        session.current_node = choice.next_question
        session.save()
        return Response({
            'question': choice.next_question.text,
            'choices': [
                {'id': ch.id, 'text': ch.text}
                for ch in choice.next_question.choices_for_question.all()
            ]
        })
    else:
        session.completed = True
        session.current_node = None
        session.save()
        return Response({'detail': 'Game completed. You can now retrieve your result.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_result(request, session_id):
    """
    Return the final result/diagnosis for a completed game session.
    """
    session = get_object_or_404(GameSession, session_id=session_id, user=request.user)

    if not session.completed:
        return Response({'detail': 'Game is not yet completed.'}, status=status.HTTP_400_BAD_REQUEST)

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

    return Response({
        'result': diagnosis,
        'score': total_score,
        'choices_made': [
            {
                'question': log.question.text,
                'choice': log.choice.text,
                'score_given': log.score_given
            } for log in logs
        ]
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_session(request, session_id):
    """
    Clear a game session and its choice logs to allow replaying the game.
    """
    session = get_object_or_404(GameSession, session_id=session_id, user=request.user)

    # Delete related choice logs first
    ChoiceLog.objects.filter(session=session).delete()
    session.delete()

    return Response({'detail': 'Game session and logs cleared. You may start a new game.'}, status=status.HTTP_204_NO_CONTENT)
