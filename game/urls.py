from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_game, name='start_game'),
    path('question/<str:session_id>/', views.get_question, name='get_question'),
    path('submit/<str:session_id>/', views.submit_choice, name='submit_choice'),
    path('result/<str:session_id>/', views.get_result, name='get_result'),
    path('clear/<str:session_id>/', views.clear_session, name='clear_session'),
]
