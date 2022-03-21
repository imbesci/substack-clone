from django.shortcuts import render, redirect
from .models import Article
from .forms import CreateArticle
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
# Create your views here.

def articles_authors(request):
    articles = Article.objects.all().filter(is_draft=False).order_by("-date")
    return render(request, 'articles/article_authors.html', context = { 'articles' : articles } )


def full_article(request, slug):
    article = Article.objects.get(slug= slug)
    article.udpate_views()
    return render(request, "articles/full_article.html" , context = { 'article' : article } )


@login_required(redirect_field_name='auth_failed', login_url= 'accounts:login')
def create_article(request):
    context = {'isCreate' : True }
    if request.POST:
        form = CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            if request.POST.get('saveAsDraft'):
                form.is_draft = True
                form.save()
                return redirect('articles:authors')
            elif form.generate_slug():
                form.slug = form.generate_slug()
                form.save()
                return redirect('articles:full', slug=form.slug)
            else:
                keys = list(request.POST)
                data = {}
                for key in keys:
                    data[key] = request.POST.get(key)
                form = CreateArticle(data, instance=request.user)
                context['articleForm'] = form
    else:
        articleForm = CreateArticle()
        context['articleForm'] = articleForm

    return render(request, 'articles/article_creation.html', context = context)


def articles_genre(request):
    genre = request.GET.get('genre').capitalize()
    genreArticles = Article.objects.all().filter(topic=genre).order_by("-date")
    context = {
        'genre' : genre,
        'genreArticles' : genreArticles
    }
    return render(request, 'articles/genres.html', context=context )

@login_required(redirect_field_name='auth_failed', login_url= 'accounts:login')
def update_article(request, key):
    if request.POST:
        article = Article.objects.get(pk=key)
        form = CreateArticle(request.POST, request.FILES, instance = article)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            if request.POST.get('saveAsDraft'):
                form.is_draft = True
                form.save()
                return redirect('accounts:profile')
            elif form.generate_slug():
                form.slug = form.generate_slug()
                form.is_draft = False
                form.save()
                return redirect('articles:full', slug=form.slug)
            else:
                return HttpResponseNotFound("<h2>Oops, something happened and we're not sure what...</h2>")
            
    else:
        article = Article.objects.get(pk=key)
        articleForm = CreateArticle(instance = article)
    return render(request, 'articles/article_creation.html', context = { 'articleForm' : articleForm } )

@login_required(redirect_field_name='auth_failed', login_url= 'accounts:login')
def view_drafts(request):
    drafts = Article.objects.all().filter(author = request.user).filter(is_draft = True)

    context = {
        'drafts': drafts
    }
    return render(request, 'articles/current_drafts.html', context = context)
