from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Question, Choice, Category

class IndexView(generic.ListView):
    model = Category
    template_name = "polls/index.html"
    context_object_name = "categories"

    def get_queryset(self):
        """Return all categories ordered by name."""
        return Category.objects.order_by("name")

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def all_questions_detail(request):
    latest_question_list = Question.objects.order_by("pub_date")[:15]
    return render(request, "polls/detail.html", {
        "latest_question_list": latest_question_list,
    })

def vote(request, question_id):
    latest_question_list = Question.objects.order_by("pub_date")[:15]
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        error_message = "You didn't select a choice."
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        error_message = None

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON response for AJAX requests
        if error_message:
            return JsonResponse({
                'success': False,
                'error': error_message
            })
        else:
            return JsonResponse({
                'success': True,
                'message': 'Vote enregistré avec succès !'
            })
    else:
        # Return normal response for regular form submissions
        if error_message:
            return render(
                request,
                "polls/detail.html",
                {
                    "latest_question_list": latest_question_list,
                    "error_message": error_message,
                    "error_question_id": question.id,
                },
            )
        else:
            return render(
                request,
                "polls/detail.html",
                {
                    "latest_question_list": latest_question_list,
                    "success_message": f"Votre vote pour '{question.question_text}' a été enregistré !",
                    "voted_question_id": question.id,
                },
            )

def questions_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    latest_question_list = Question.objects.filter(category=category).order_by("pub_date")
    return render(request, "polls/detail.html", {
        "latest_question_list": latest_question_list,
        "category": category,
    })

def results_summary(request):
    questions = Question.objects.all().order_by("pub_date")
    return render(request, "polls/results_summary.html", {
        "questions": questions,
    })

