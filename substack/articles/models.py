from fcntl import F_SEAL_SEAL
from django.db import models
import datetime
from django.forms import ValidationError
from accounts.models import SubstackUser
import re
from ckeditor.fields import RichTextFormField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Article(models.Model):
    title =         models.CharField(max_length=200)
    description =   models.CharField(max_length = 150)
    body =          RichTextUploadingField(blank = True, null=True)
    # body =          models.TextField()
    slug =          models.SlugField()
    date =          models.DateTimeField(auto_now_add = True)
    last_edited =   models.DateTimeField(auto_now = True)
    thumbnail =     models.ImageField(default='logo.png', blank = True)
    topicslist = [
        ("Business","Business"),
        ("Culinary", "Culinary"),
        ("Culture", "Culture"),
        ("Health", "Health"),
        ("Literature", "Literature"),
        ("Other", "Other"),
        ("Politics", "Politics"),
        ("Sports", "Sports"),
    ]
    topic =         models.CharField(max_length=30, null=True, blank=True, choices=topicslist)
    author =        models.ForeignKey(SubstackUser,  null=True, blank=True, on_delete=models.CASCADE)
    views =         models.IntegerField(default=0)
    is_draft =      models.BooleanField(default=False)

    REQUIRED_FIELDS = ['title',]

    def __str__(self):
        return self.title
    
    def article_snippet(self):
        wordsList = self.body.split(' ')[0:30]
        return ' '.join(wordsList) + '...'

    def MonthDayYear(self):
        months= {'01':'Jan', '02':'Feb', '03':'Mar', 
                 '04':'Apr', '05':'May', '06':'Jun', 
                 '07':'Jul', '08':'Aug', '09':'Sep', 
                 '10':'Oct', '11':'Nov', '12':'Dec'}
        mdy = self.date.strftime("%m-%d-%y").split('-')
        return f"{months[mdy[0]]} {mdy[1]}"

    def MDYdate(self):
        months= {'01':'Jan', '02':'Feb', '03':'Mar', 
                '04':'Apr', '05':'May', '06':'Jun', 
                '07':'Jul', '08':'Aug', '09':'Sep', 
                '10':'Oct', '11':'Nov', '12':'Dec'}
        mdy = self.date.strftime("%m_%d_%Y_%-I_%M_%p").split('_')
        return f"{months[mdy[0]]} {mdy[1]}, {mdy[2]}"
    
    def MDYdate_time(self):
        months= {'01':'Jan', '02':'Feb', '03':'Mar', 
                '04':'Apr', '05':'May', '06':'Jun', 
                '07':'Jul', '08':'Aug', '09':'Sep', 
                '10':'Oct', '11':'Nov', '12':'Dec'}
        mdy = self.date.strftime("%m_%d_%Y_%-I_%M_%p").split('_')
        return f"{months[mdy[0]]} {mdy[1]} at {mdy[3]}:{mdy[4]}{mdy[5]}"


    def MDYlast_edited(self):
        months= {'01':'January', '02':'February', '03':'March', 
                '04':'April', '05':'May', '06':'June', 
                '07':'July', '08':'August', '09':'September', 
                '10':'October', '11':'November', '12':'December'}
        mdy = self.last_edited.strftime("%m_%d_%Y_%-I_%M_%p").split('_')
        return f"{months[mdy[0]]} {mdy[1]} at {mdy[3]}:{mdy[4]}{mdy[5]}"

    def generate_slug(self):
        stripped = self.title.strip()
        cleanedTitle = re.sub(r"[^a-zA-Z0-9 :]+",'', stripped).split(' ')[0:7]
        cleanedSlug =  '-'.join(cleanedTitle).lower()
        number = 1
        while Article.objects.all().filter(author_id=self.author.pk).filter(slug=cleanedSlug):
                cleanedSlug += str(number)
                number +=1
        return cleanedSlug

    def create_slug_url(self):
        return f"/articles/{self.slug}/"

    def udpate_views(self):
        self.views = self.views + 1
        self.save()
        return self.views

    def shorten_desc(self):
        desc = self.description[0:100]
        return desc+'...'
