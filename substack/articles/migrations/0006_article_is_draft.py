# Generated by Django 4.0.2 on 2022-03-11 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_article_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_draft',
            field=models.BooleanField(default=False),
        ),
    ]
