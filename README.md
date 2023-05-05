# Capstone project for CS50’s Web Programming with Python and JavaScript course

**Table of Contents**
- [Project Overview](#project-overview)
- [How to Run](#how-to-run)
- [Distinctiveness and Complexity](#distinctiveness-and-complexity)
- [Project Files](#project-files)
  - [`trivia_showdown/models.py`](#trivia_showdownmodelspy)
  - [`trivia_showdown/forms.py`](#trivia_showdownformspy)
  - [`trivia_showdown/admin.py`](#trivia_showdownadminpy)
  - [`trivia_showdown/context_processors.py`](#trivia_showdowncontext_processorspy)
  - [`trivia_showdown/calculations.py`](#trivia_showdowncalculationspy)
  - [`trivia_showdown/views.py`](#trivia_showdownviewspy)
  - [`trivia_showdown/templates` directory](#trivia_showdowntemplates-directory)
  - [`trivia_showdown/static` directory](#trivia_showdownstatic-directory)


## Project Overview
A trivia/quiz style web application with a leaderboard system. Built with Django and JavaScript, with styling help from [Bulma CSS](https://bulma.io/).

## How to Run
1. Download the source code from GitHub and extract to a folder of your choosing
2. Enter the project directory and open your computer's terminal
3. You have two options, if you want to start the project with the included test data and fake users, simply run `python manage.py runserver`, if you instead want to start with an empty database, delete the `db.sqlite3` file, and run the following commands: `python manage.py makemigrations`, `python manage.py migrate`, and finally `python manage.py runserver`
4. Open your browser and go to `http://127.0.0.1:8000`


## Distinctiveness and Complexity
I believe the project satisfies the distinctiveness and complexity requirements because of a number of new functionalities it introduces. There is usage of an external public API, which requires new methods of retrieving and storing data that has not been present in the course so far, as well as handling possible errors that may arise when working with an external API. In addition, there are also more complex logic on the frontend.

On the Django side of things, this project introduces the usage of Python's [regular expression operations](https://docs.python.org/3/library/re.html) module to slugify strings, the usage of Django's [messages framework](https://docs.djangoproject.com/en/4.1/ref/contrib/messages/) to display messages to users on the frontend, and it was the first time that I wrote code that returns a [JSON response](https://docs.djangoproject.com/en/4.2/ref/request-response/#jsonresponse-objects) to the frontend. 

Possibly adding to the complexity of the project, I wrote Django views that are not directly used by the `URLs.py` file, as the purpose of these views are to be functions that other views call on. I also made use of a custom `context_processor` because I found it useful for different template files to consume the same data without having to load any additional tags, and without needing to pass the same context in different views—reducing code repetition.

In the template files of this project, I try to minimize code repetition by using Django's `{% include %}` to represent snippets of Django HTML as reusable components, reducing the need to re-type commonly used HTML. Also in the Django templates, I made us of template tags such as `{% regroup %}` to organize data on the frontend, minimizing the need for server computation.

In JavaScript, I made use of the [`setInterval()`](https://developer.mozilla.org/en-US/docs/Web/API/setInterval) API, which required me to learn more about the JavaScript [call stack](https://developer.mozilla.org/en-US/docs/Glossary/Call_Stack) and how to write code that executes after a delay. Also on the frontend, this project involves the frequent use of the HTML `[data-*]` attributes to allow JavaScript to query for certain elements without the need to use IDs or classes, allowing the JavaScript code to be cleaner, and hopefully more readable.

## Project Files
### `trivia_showdown/models.py`
All the Django models used in the project:
- `User`: simply passes Django's built-in `AbstractUser` model.
- `Question`: represents a question with the question itself, its category, three wrong answers, one correct answer, and an integer (1, 2, or 3) to represent the question's difficulty.
- `QuestionCategory`: represents a question's category with a name and a slug.
- `UserAnswer`: represents a user's answer to a question, and whether or not the user had answered correctly.

### `trivia_showdown/forms.py`
Contains a Django form called `QuestionForm` to safely handle user inputs when submitting answers.

### `trivia_showdown/admin.py`
Here in the `admin.py` file, we register Django models so that instances of the models can be created, modified, and deleted in Django's admin interface.

### `trivia_showdown/context_processors.py`
Returns a dictionary containing the site's title, and either a `user` object or `None` depending on the user's authentication status. I have registered this context processor in `settings.py` as `trivia_showdown.context_processors.site_info_metadata`.

### `trivia_showdown/calculations.py`
Contains a single function called `calculate_total_score`, which accepts as arguments the number of correct answers and the number of incorrect answers a user has given, finds the ratio of correct to incorrect answers, multiplies the ratio by 1000 and returns the result as the user's total score.

### `trivia_showdown/views.py`
Contains the Django views for the project:
- `index`: the homepage of the webapp, upon calling it an API request is made to [the-trivia-api.com/api/categories](https://the-trivia-api.com/api/categories) to check all available question categories and store them in our database. A grid of all available question categories is then rendered on the hompage for the user to choose and play.
- `register_view`, `login_view`, and `logout_view`: these views are responsible for handling user registrations, logins, and logouts respectively.
- `query_user_answers`: queries the database for user answers and returns data according to the parameter `item_to_return`.
- `get_data`: returns JSON data from an API.
- `slugify`: accepts a string as a parameter and returns a slugified string, which can then be used in URL parameters in a clean way.
- `profile`: renders the profile page of a user.
- `leaderboard`: renders the leaderboard page with pagination. Queries for the total scores of all users using the previously mentioned `query_user_answer` view, and the sorting will be handled on the frontend.
- `get_question_by_categ`: makes an API request and returns one question with the same category as specified in the parameter.
- `quiz`: accepts a `category_slug` parameter, returns a first question using the `get_question_by_categ` view, and renders the quiz template.
- `submit_answer`: handles the submission of user answers, saves them to the database in the form of `UserAnswer`, and returns a `JsonResponse`.

### `trivia_showdown/templates` directory
- `layout.html`: the layout for other templates, contains meta tags, navbar, and site-wide scripts.
- `index.html`: the homepage.
- `register.html`: template with the registration form.
- `login.html`: template with the login form.
- `quiz.html`: template for quizzes.
- `profile.html`: template to display user profiles and displays the user's total score, and the score the user has in each category, all done using Django's `regroup` and some JavaScript DOM manipulation.
- `leaderboard.html`: template to display the leaderboard, sorting is handled using Django's `dictsortreversed`.
- `templates/components`: this directory contains commonly used template snippets as components for other templates to include them in.

### `trivia_showdown/static` directory
- `static/css`: contains all the styling for the webapp.
- `static/scripts`:
  - `bulma_components.js`: script to handle frontend components such as the navbar and notification banners.
  - `redirect_random_categ.js`: script to redirect the user to a quiz with a random category.
  - `quiz.js`: script file used by the `quiz.html` template to handle DOM manipulation, API requests, user inputs, answer button placement randomization, question timer, and pagination from one question to the next.
