from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, Http404, HttpResponseRedirect
# from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """ Return the last five published questions (not including those set to be published in the future)"""
        # return Question.objects.order_by("-pub_date")[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:10]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())
    

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


    

##########################################################################
## Constructing the views specifically (not with the django generic views)
##########################################################################
# def index(request: HttpRequest):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5] #use the API to return the last 5 Question objects that are ordered by by pub_date (DESC)
    
#     context = {"latest_question_list" : latest_question_list}
#     return render(request=request, template_name="polls/index.html", context=context)

#     # template = loader.get_template("polls/index.html")
#     # context = {
#     #     "latest_question_list": latest_question_list
#     # }
#     # return HttpResponse(template.render(context=context, request=request))

#     # output = ", ".join([q.question_text for q in latest_question_list])
#     # return HttpResponse(output)


# def detail(request: HttpRequest, question_id):
#     # return HttpResponse(f"You're looking at question {question_id}")

#     ## return a conditional 404 if the object does not exist given the primary key (pk) requested
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exists, much like the limit.")
    
#     # return render(request, "polls/detail.html", {"question": question} )

#     question=get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})


# def results(request: HttpRequest, question_id):
#     # response = f"You're looking at the results of question {question_id}"
#     # return HttpResponse(response)

#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {"question": question})


## still needed in this specific form, even when constructing views using the class/generic django views
def vote(request: HttpRequest, question_id):
    # return HttpResponse(f"You're voting on question {question_id}")
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice. You dummy.",
            },
        )

    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

       
