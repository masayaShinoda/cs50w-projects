# Generated by Django 4.1 on 2023-04-07 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trivia_showdown', '0007_alter_question_opt2'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('correct', 'Correct'), ('incorrect', 'Incorrect')], max_length=10)),
                ('question_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trivia_showdown.questioncategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
