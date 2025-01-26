from django.urls import path

from . import views #import the views.py file from the current dir (../polls), the app's dir

app_name = "polls" # define a namespace to associate these specific urls to this specific app (../polls)
# urlpatterns = [
#     path(route="", view=views.index, name="index"), #define a route for the pagination, from the imported views/pages define what it show display, and give a name
#     path(route="<int:question_id>/", view=views.detail, name="detail"),
#     path("<int:question_id>/results/", views.results, name="results"),
#     path("<int:question_id>/vote/", views.vote, name="vote"),
# ]

#create the url (patterns) with the Views/ListViews/DetailView constructor(?)
urlpatterns = [
    path(route="", view=views.IndexView.as_view(), name="index"), #define a route for the pagination, from the imported views/pages define what it show display, and give a name
    path(route="<int:pk>/", view=views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]

