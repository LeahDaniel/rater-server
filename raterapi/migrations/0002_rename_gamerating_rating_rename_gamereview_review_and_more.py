# Generated by Django 4.0.1 on 2022-02-02 20:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('raterapi', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GameRating',
            new_name='Rating',
        ),
        migrations.RenameModel(
            old_name='GameReview',
            new_name='Review',
        ),
        migrations.RemoveField(
            model_name='game',
            name='user',
        ),
        migrations.AddField(
            model_name='game',
            name='categories',
            field=models.ManyToManyField(related_name='attending', through='raterapi.GameCategory', to='raterapi.Category'),
        ),
    ]
