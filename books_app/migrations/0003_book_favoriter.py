# Generated by Django 2.2 on 2021-02-08 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0002_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='favoriter',
            field=models.ManyToManyField(related_name='favorited_books', to='books_app.User'),
        ),
    ]
