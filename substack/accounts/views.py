from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate, get_user_model
from httplib2 import Http
from .models import SubstackUser
from .forms import SubstackUserCreation, SubstackAuthenticationForm, SubstackUpdateForm, SubstackAccountUpdateFormset, SubstackAccountUpdate
from django.contrib.auth.decorators import login_required
from articles.models import Article
from articles.views import create_article

# Create your views here.
def login_screen(request):
    user = request.user
    if user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = SubstackAuthenticationForm(request.POST)
        if form.is_valid:
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email = email, password = password)
            if user:
                login(request, user)
                if request.POST.get('auth_failed'):
                    return redirect(request.POST.get('auth_failed'))
                return redirect("accounts:dashboard")
    else:
        form = SubstackAuthenticationForm()
    return render(request, 'accounts/login_webpage.html', context = { 'form': form } )

def create_account(request):
    if request.method == 'POST':
        form = SubstackUserCreation(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('articles:create')
    else:
        form = SubstackUserCreation()
    return render(request, 'accounts/create_account.html', context = { 'form': form } )


def logout_view(request):
    if request.user:
        logout(request)
        return redirect('homepage')
    else:
        return redirect('homepage')
        

def send_to_login(request):
    return redirect('accounts:login')

@login_required(login_url='accounts:login', redirect_field_name='auth_failed')
def account_dashboard(request):
    if request.method == "POST":
        draftKey = request.POST.get('draftRedirect')
        draftData = Article.objects.get(pk=draftKey)
        return render(request, 'articles/article_creation.html', context = {'draftData' : draftData } )

    context = {}
    account = request.user #retrieve the user
    context['account'] = account 
    numArticles = len(list(Article.objects.all().filter(author = account.pk)))

    if numArticles >0:
        firstArticle = Article.objects.filter(author = account.pk, is_draft=False).order_by("-date")[0]
        context['firstArticle'] = firstArticle
    else:
        context['firstArticle'] = None

    if numArticles>1:
        remainingArticles = Article.objects.filter(author = account.pk, is_draft=False).order_by("-date")[1:]
        context['remainingArticles'] = remainingArticles

    recentDrafts = Article.objects.filter(author = account.pk, is_draft=True).order_by("-date")[0:3]
    context['drafts'] = recentDrafts
    context['isProfile'] = True


    return render(request, 'accounts/dashboard.html', context=context)


##Code below uses HTMX snippets         Account Updating ##
@login_required(login_url='accounts:login', redirect_field_name='auth_failed')
def show_account(request):
    pk = request.user.pk
    user = SubstackUser.objects.get(pk=pk)
    context = {
        'user' : user,
        'isDetail': True
    }
    return render(request, 'accounts/account_details.html', context)

@login_required(login_url='accounts:login', redirect_field_name='auth_failed')
def detail_snippet(request):
    pk = request.user.pk
    user = SubstackUser.objects.get(pk=pk)
    form = SubstackAccountUpdate(instance=user)

    if request.method == "POST":
        form = SubstackAccountUpdate(request.POST, instance = user)
        if form.is_valid():
            form.save()
            redirect('accounts:detail-snippet')
        else:
            redirect('accounts:edit-snippet', user)

    context= {
        'form' : form,
        'user' : user
    } 
    return render(request, 'accounts/account_details.html', context)

@login_required(login_url='accounts:login', redirect_field_name='auth_failed')
def edit_snippet(request): 
    pk = request.user.pk
    user = SubstackUser.objects.get(pk=pk)

    form = SubstackAccountUpdate(instance=user)
    context= {
        'form' : form,
        'user' : user
    }
    return render(request, 'accounts/snippets/edit_snippet.html', context)

def verify_email(request):  #verify if email is taken per key input
        email = request.POST.get('email')
        if get_user_model().objects.filter(email = email).exists():
            return HttpResponse(
                "<div id='emailverification' style='color:red;'>This email is taken!</div>"
            )
        else:
            return HttpResponse(
                "<div id='emailverification' style='color:green;'>This email is available!</div>"
            )