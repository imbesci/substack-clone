from django import forms
from . import models


#add form for making new articles
class CreateArticle(forms.ModelForm):
    title = forms.CharField(max_length = 200, widget = forms.Textarea(attrs = {'placeholder': 'Enter title...', 'min_length':1, 'rows':1}))
    description = forms.CharField(widget = forms.Textarea(attrs = {'placeholder': 'Write a brief description...', 'rows':'2', }))

    class Meta:
        model = models.Article
        fields = ['title', 'description', 'body', 'thumbnail', 'topic' ]
        help_texts = {
                    'title': 'Please choose a unique title.',
                    }
   