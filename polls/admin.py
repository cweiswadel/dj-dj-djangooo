from django.contrib import admin

# Register your models here.
from .models import ( 
    Question, Choice,
    # QuestionSecond, ChoiceSecond
)

# admin.site.register(Question)
# admin.site.register(Choice)


## This is a way better to handle PK to FK relations
    ## Example: Define a Question(Second) model that has a Choice(Second) FK dependency, use this InLine Model definition
    ##  Within this InLine definition on /admin/ a Question can be made and within the same page/in-line, you can define the FK Choice models
    ## ^^ This creates way better visibility during configurations
class ChoiceInLine(admin.TabularInline): #this creates the 'InLine' ability of the given Choice model
    model= Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin): #define that the ChoiceInLine model belongs to the admin page of Question
    inlines=[ChoiceInLine]

admin.site.register(Question, QuestionAdmin) #define the model and what its equivalent AdminModel
admin.site.register(Choice)