from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("question/<int:question_id>/answer/", views.answer_question, name="answer_question"),
    path("answer/<int:answer_id>/evidence/", views.add_evidence, name="add_evidence"),
    path("submit/", views.submit_assessment, name="submit_assessment"),
    path("summary/", views.summary, name="summary"),
]
