# Generated by Django 4.1 on 2023-04-11 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trivia_showdown', '0008_useranswer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useranswer',
            options={'ordering': ['question_category']},
        ),
    ]
