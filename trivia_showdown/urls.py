from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("profile", views.profile, name="profile"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("leaderboard", views.leaderboard, name="leaderboard"),
    path("quiz", views.quiz_view, name="quiz"),
    path("quiz/<str:category_slug>", views.quiz_view, name="quiz"),
    path("get-question-by-category/<str:category_slug>", views.get_question_by_categ, name="get_question_by_category"),
    path("submit-answer/<str:category_slug>/<str:status>", views.submit_answer, name="submit_answer")
]