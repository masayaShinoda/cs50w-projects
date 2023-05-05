from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    pass

class Question(models.Model):
    # question & answer is required, at least two answer options is required
    question = models.CharField(max_length=200)
    opt1 = models.CharField(max_length=200)
    opt2 = models.CharField(max_length=200, null=True)
    opt3 = models.CharField(max_length=200, null=True)
    answer = models.CharField(max_length=200)
    
    difficulty = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(3)])
    category = models.ForeignKey("QuestionCategory", on_delete=models.CASCADE)

    def __str__(self):
        return f"""{self.id}. {self.question}"""
    
    def clean(self):
        # make sure that at least two options for the question are provided
        options = [self.opt1, self.opt2, self.opt3]
        if len(options) < 2:
            raise ValidationError("At least two answer options for the question are required.")

    
class QuestionCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, primary_key=True)

    def __str__(self):
        return f"""{self.name}"""
    
class UserAnswer(models.Model):
    # keep score of a user's answer based on category
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE)

    status = models.CharField(max_length=10, choices=[
        ("correct", "Correct"),
        ("incorrect", "Incorrect"),
    ])

    class Meta:
        ordering = ["user", "question_category", "status"]

    def __str__(self):
        return f"""{self.user} | {self.question_category} | {self.status}"""