from csv import list_dialects
from django import forms
from . import models


#add form for making new articles
class CreateArticle(forms.ModelForm):
    title = forms.CharField(max_length = 200, widget = forms.Textarea(attrs = {'placeholder': 'Choose a unique title for your work', 'min_length':1, 'size': 50}))
    description = forms.CharField(widget = forms.Textarea(attrs = {'placeholder': 'Write a brief descrption...', 'rows':'3', 'cols': '70'}))
    # body = forms.CharField(widget = forms.Textarea(attrs = {'placeholder': 'Write the body of your article...', 'rows':'10', 'cols': '100'},))

    class Meta:
        model = models.Article
        fields = ['title', 'description', 'body', 'thumbnail', 'topic' ]
        help_texts = {
                    'title': 'Please choose a unique title.',
                    }
   