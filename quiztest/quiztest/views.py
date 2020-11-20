from typing import List, Any

from django.shortcuts import render
from .models import Login
from django.db import connection
from pytrivia import Category, Diffculty, Trivia, Type
from django.http import HttpResponse

correct = ''


def get_ques():
    global correct
    my_api = Trivia(True)
    response = my_api.request(1, Category.Computers, Diffculty.Easy, Type.Multiple_Choice)
    response = response['results']
    sub_lis = [response[0]['question']]
    ques_opt = [response[0]['correct_answer']]
    correct = response[0]['correct_answer']
    ques_opt.extend(response[0]['incorrect_answers'])
    ques_opt.sort()
    sub_lis.extend(ques_opt)
    return sub_lis


def question(request):
    sub = get_ques()
    return render(request, "quiz.html", {'ques_opt': sub})


def answer_valid(request):
    if request.method == 'POST':
        selected = request.POST['option']
        if selected == correct:
            for i in range(9):
                return question(request)
    return question(request)


def fun_login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname', False)
        user_pass = request.POST.get('psw', False)
        cur = connection.cursor()
        cur.execute('select user_id,password from login_details where user_id=%s', [uname])
        results = cur.fetchall()
        if len(results) != 0:
            if str(uname) == str(results[0][0]) and str(user_pass) == str(results[0][1]):
                # request.session['username'] = uname
                return render(request, "terms.html", {'Login':results[0]})
            else:
                return render(request, "index.html", {'Error': 'Invalid Login Details'})
        else:
            return render(request, "index.html", {'Error': 'Invalid Login Details'})
    else:
        return render(request, "index.html", {'Error': 'Invalid Login Details'})
