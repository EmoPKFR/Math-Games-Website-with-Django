from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import GameLevel, GameScore
import random

def generate_problem(level):
    if level == "easy":
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        operation = random.choice(["+", "-"])
    elif level == "medium":
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        operation = random.choice(["+", "-", "*", "/"])
    elif level == 'hard':
        a = random.randint(10, 30)
        b = random.randint(10, 30)
        operation = "/"
    elif level == 'expert':
        a = random.randint(20, 50)
        b = random.randint(20, 50)
        operation = random.choice(["*", "/"])
    elif level == 'multiplication_by_5':
        a = random.randint(10, 50)
        b = 5
        operation = "*"
    elif level == 'division_by_5':
        a = random.randint(50, 200)
        b = 5
        operation = "/"
    
    problem = f"{a} {operation} {b}"

    #Calculate the answer and handle division separately
    if operation == "/":
        #Ensure we don't divide by zero
        if b == 0:
            b = random.randint(1, 10)  #or any appropriate non-zero value for your level
        answer = round(a / b, 2)  #round to 2 decimal places
    else:
        answer = eval(problem)

    return problem, answer

@login_required
def play_game(request, level_name):
    level = GameLevel.objects.get(name=level_name)

    # Reset score when switching levels
    if request.session.get("current_level") != level_name:
        request.session["score"] = 0
        request.session["current_level"] = level_name

    if "score" not in request.session:
        request.session["score"] = 0

    if request.method == "POST":
        user_answer = round(float(request.POST["answer"]), 2)
        correct_answer = round(float(request.session.get('answer')), 2)
        print(f"User answer: {user_answer}, Correct answer: {correct_answer}")

        if user_answer == correct_answer:
            request.session["score"] += 1
        else:
            # Save the score before redirecting to failure page
            save_score(request, level)
            return redirect("math_games:game_failure", level_name=level_name)
    
    problem, answer = generate_problem(level_name)
    request.session['answer'] = answer
    return render(request, "math_games/play_game.html", {"level": level, "problem": problem, "score": request.session["score"]})

@login_required
def reset_game(request, level_name):
    request.session["score"] = 0
    problem, answer = generate_problem(level_name)
    request.session['answer'] = answer
    level = GameLevel.objects.get(name=level_name)
    return render(request, "math_games/play_game.html", {"level": level, "problem": problem, "score": request.session["score"]})

def game_success(request, level_name):
    save_score(request, level_name)
    return render(request, "math_games/game_success.html", {"level_name": level_name})

def game_failure(request, level_name):
    save_score(request, level_name)
    score = request.session.get("score", 0)
    request.session["score"] = 0
    return render(request, "math_games/game_failure.html", {"level_name": level_name, "score": score})

def select_level(request):
    levels = GameLevel.objects.all()
    return render(request, "math_games/select_level.html", {"levels": levels})

def save_score(request, level_name):
    level = GameLevel.objects.get(name=level_name)
    score = request.session.get("score", 0)
    user = request.user

    game_score, created = GameScore.objects.get_or_create(user=user, level=level)

    # Update the highest_score if the current score is higher
    if score > game_score.highest_score:
        game_score.highest_score = score
    
    game_score.save()

@login_required
def leaderboard(request):
    # Retrieve the top 10 scores for each level
    levels = {}
    for level in GameLevel.objects.all():
        top_scores = GameScore.objects.filter(level=level).order_by('-highest_score')[:10]
        levels[level.name] = top_scores

    return render(request, "math_games/leaderboard.html", {"levels": levels})