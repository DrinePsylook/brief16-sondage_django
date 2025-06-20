from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("detail/", views.all_questions_detail, name="detail"),
    path("results/", views.results_summary, name="results_summary"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("category/<int:category_id>/", views.questions_by_category, name="questions_by_category"),
]