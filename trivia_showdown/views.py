from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.contrib import messages
from django.urls import reverse
from django.db import IntegrityError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import User, QuestionCategory, UserAnswer
# python requests module
import requests
# python regular expressions
import re
# function to calculate a user's score
from .calculations import calculate_total_score

template_files = {
    "index": "index.html",
    "login": "login.html",
    "register": "register.html",
    "profile": "profile.html",
    "leaderboard": "leaderboard.html",
    "quiz": "quiz.html",
}

# function to reteurn relevent UserAnswer model data
def query_user_answers(item_to_return):
    all_user_answers = UserAnswer.objects.all()

    all_correct_answers = UserAnswer.objects.filter(status="correct")
    all_incorrect_answers = UserAnswer.objects.filter(status="incorrect")

    unique_users_arr = []
    # get unqiue users from database
    for user_with_answer in UserAnswer.objects.values("user"):
        if user_with_answer not in unique_users_arr:
            unique_users_arr.append(user_with_answer)
    
    # array of dictionaries that store user-correct_answers_count pairs
    answers_by_user = []
    for unique_user in unique_users_arr:
        # use dictionary so we can dictsort later
        answers_by_user.append({
            "username": User.objects.get(id=unique_user['user']).username,
            "all_answers_by_user": all_user_answers.filter(user=unique_user['user']),
            "correct_answers": all_correct_answers.filter(user=unique_user['user']),
            "incorrect_answers": all_incorrect_answers.filter(user=unique_user['user']),
            "correct_answers_count": all_correct_answers.filter(user=unique_user['user']).count(),
            "incorrect_answers_count": all_incorrect_answers.filter(user=unique_user['user']).count()
        })

    if(item_to_return == "answers_by_user"):
        return answers_by_user
    
    if(item_to_return == "users_total_scores"):
        # array of dictionaries that store { username, total_score }
        users_total_scores = []
        for item in answers_by_user:
            users_total_scores.append({
                "username": item["username"],
                "total_score": calculate_total_score(item["correct_answers_count"], item["incorrect_answers_count"])
            })
        return users_total_scores


# function to get data from an API
def get_data(url, params=None): # params are optional
    response = requests.get(url, params=params)

    # if response is OK
    if response.status_code == 200:
        return response.json()
    else:
        return None

# function to slugify string
def slugify(string):
    string = string.lower().strip()
    string = re.sub(r'&', '_and_', string)
    string = re.sub(r'[\W_]+', '_', string)
    return string


def index(request):
    # get available categories from API
    api_url = "https://the-trivia-api.com/api/categories"

    try:
        api_categories = get_data(api_url)
        # check if data exists
        if api_categories:
            for item in api_categories.keys():
                # get category if it exists, or create one if it doesn't, returned values are assigned to `category` or `created` accordingly
                category, created = QuestionCategory.objects.get_or_create(
                    name = item,
                    slug = slugify(item)
                )
        else:
            messages.add_message(request, messages.ERROR, "No data was returned from the API.")
    except Exception as exception:
        messages.add_message(request, messages.ERROR, f"""There was a problem attempting to connect to the API: {exception}""")

    # get the questions from our database
    categories = QuestionCategory.objects.all()

    # context
    data = {
        "categories": categories,
    }

    return render(request, template_files["index"], data)

def login_view(request):
    if request.method == "POST":
        # attempt to sign the user in
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        # check if auth is successful
        if user is not None:
            login(request, user)
            return redirect(reverse("index"))
        else:
            messages.add_message(request, messages.ERROR, "Invalid username and/or password.")
            return render(request, template_files["login"])
        
    else:
        return render(request, template_files["login"])
    
def logout_view(request):
    logout(request)
    return redirect(reverse("index"))
    
def register_view(request):
    if request.user.is_authenticated:
        # if user is already signed in, redirect to index view with a message
        messages.add_message(request, messages.ERROR, "You are already logged in. Please logout to create a new account.")
        return redirect(reverse("index"))
    else:
        if request.method == "POST":
            username = request.POST["username"]
            email = request.POST["email"]
            
            # check if `password` matches `confirm password`
            password = request.POST["password"]
            confirm_password = request.POST["confirm_password"]
            if password != confirm_password:
                messages.add_message(request, messages.ERROR, "Password and Confirm Password must match.")
                return render(request, template_files["register"])
                
            # attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                messages.add_message(request, messages.ERROR, "Username has been taken. Please try again.")
                return render(request, template_files["register"])
            
            # after user is created, sign em' in!
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "Your account has been successfully created.")
            return redirect(reverse("index"))

        else:
            return render(request, template_files["register"])
    
    
def profile(request, username=None): # username arg is optional
    user = request.user

    # variable to store user's total score
    user_total_score = None
    # variable to store all answers by user
    user_all_answers = []

    # check if username param in the URL exists
    if username is not None:
        for item in query_user_answers("answers_by_user"):
            if item["username"] == username:
                user_all_answers.append(item)

        for item in query_user_answers("users_total_scores"):
            if item["username"] == username:
                user_total_score = item["total_score"]
                
        data = {
            "profile_user": User.objects.get(username=username),
            "user_all_answers": user_all_answers if user_all_answers else None,
            "user_total_score": user_total_score if user_total_score else None,
        }
    else:
        # no username param specified (example: /profile/)
        if user.is_authenticated:
            # redirect to user's own profile if no profile specified
            return redirect(reverse("profile", kwargs={"username": user.username}))
        else:
            # ask the user to sign in
            messages.add_message(request, messages.WARNING, "Please sign in to continue.")
            return redirect(reverse("login"))

    return render(request, template_files["profile"], data)

def leaderboard(request):
    users_total_scores = query_user_answers("users_total_scores")

    # get `page` URL param, it none exists, default to 1
    page_number = request.GET.get("page", 1)
    # show 10 users per page on the leaderboard
    paginator = Paginator(users_total_scores, 10)

    try:
        leaderboard_content = paginator.page(page_number)
    except PageNotAnInteger:
        # for invalid parameters, return first page
        leaderboard_content = paginator.page(1)
    except EmptyPage:
        # for page number greater than available pages, return the last page
        leaderboard_content = paginator.page(paginator.num_pages)

    data = {
        # "user": user if user is not None else None,
        "leaderboard_content": leaderboard_content,
    }

    return render(request, template_files["leaderboard"], data)

def quiz_view(request, category_slug=None): # category is optional
    # only allow quizing for signed in users
    if request.user.is_authenticated:
        # check if category slug exists in URL
        if category_slug is not None:
            data = {
                "category": QuestionCategory.objects.get(slug=category_slug),
                "category_slug": category_slug
            }

            return render(request, template_files["quiz"], data)
        else:
            # no category specified, redirect to homepage, "choose category" section
            return redirect(reverse("index") + "#categories")

    else:
        # ask the user to sign in
        messages.add_message(request, messages.WARNING, "Please sign in to continue.")
        return redirect(reverse("login"))
    

@require_GET
@login_required
def get_question_by_categ(request, category_slug):
    
    # get available categories from API
    api_url = "https://the-trivia-api.com/api/questions"
    api_params = {"limit": 1, "categories": category_slug}

    try:
        api_data = get_data(api_url, api_params)
        # check if data exists
        if api_data:
            # dictionary that maps "easy", "medium", and "hard" form the API to 1, 2, 3 respectively
            difficulty_index = {
                "easy": 1,
                "medium": 2,
                "hard": 3
            }

            for item in api_data:
                # map the difficulty to difficulty_index
                difficulty = difficulty_index.get(item["difficulty"], 1)

                # JSON response to the frontend
                return JsonResponse({
                    "question": item["question"],
                    "opt1": item["incorrectAnswers"][0], 
                    "opt2": item["incorrectAnswers"][1], 
                    "opt3": item["incorrectAnswers"][2], 
                    "answer": item["correctAnswer"],
                    "difficulty": difficulty
                })

        else:
            messages.add_message(request, messages.ERROR, "No data was returned from the API.")
            return redirect(reverse("index"))
    except Exception as exception:
        messages.add_message(request, messages.ERROR, f"""There was a problem attempting to connect to the API: {exception}""")
        return redirect(reverse("index"))

@login_required
def submit_answer(request, category_slug, status):
    if request.method == "POST":
        user = request.user
        if user.is_authenticated:
            # check valid category_slug
            if QuestionCategory.objects.filter(slug=category_slug).exists():
                if status == "correct":
                    user_answer_status = "correct"
                else:
                    user_answer_status = "incorrect"

                user_answer = UserAnswer(
                    user = user,
                    question_category = QuestionCategory.objects.get(slug=category_slug),
                    status = user_answer_status
                )
                user_answer.save()

                return JsonResponse({
                    "message": "Accepted"
                })
        else:
            messages.add_message(request, messages.ERROR, "You are not authorized to complete this action.")
            return redirect(reverse("index"))
    else:
        messages.add_message(request, messages.ERROR, "You are not authorized to complete this action.")
        return redirect(reverse("index"))