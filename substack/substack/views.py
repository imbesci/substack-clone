from django.shortcuts import render
from articles.models import Article 
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile
from django.forms.models import model_to_dict
import random

class ExtendedEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, ImageFieldFile):
            return str(o)
        else:
            return super().default(o)


def homepage(request):
    context = {}

    if request.POST:
        filter = request.POST.get('filter')
        filteredarticles = list(Article.objects.all().filter(is_draft = False, topic = filter).order_by("-date"))
        for i, article in enumerate(filteredarticles):
            filteredarticles[i] = model_to_dict(article)
            filteredarticles[i]['thumburl'] = article.thumbnail.url
            filteredarticles[i]['description'] = article.shorten_desc()
            filteredarticles[i]['slug'] = article.create_slug_url()
            filteredarticles[i]['date'] = article.MDYdate()
            filteredarticles[i]['author'] = article.author.username
        return JsonResponse({'filtered' : filteredarticles }, encoder = ExtendedEncoder, status=200)
    
    else:
        allarticles = list(Article.objects.all().filter(is_draft=False))
        FEATUREDQUANTITY = 7
        featuredArticles = []
        for i in range(FEATUREDQUANTITY):
            k = random.randint(0, (len(allarticles)-1))
            featuredArticles.append(allarticles[k])
            allarticles.pop(k) 
        context['features'] = featuredArticles

    return render(request, 'homepage.html', context=context)