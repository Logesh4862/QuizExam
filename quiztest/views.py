from typing import List, Any

from django.shortcuts import render
from .models import Login
from django.db import connection
from pytrivia import Category, Diffculty, Trivia, Type
from django.http import HttpResponse
import time

correct = ''
count = 10
sub = []
mark = 0


def create_user(request):
    u_name = request.POST['uname']
    u_pass = request.POST['psw']
    cursor = connection.cursor()
    cursor.execute('select * from login_details where user_id=%s', [u_name])
    result = cursor.fetchall()
    if len(result) == 0:
        cursor.execute("insert into login_details(id,user_id,password)"
                       "values(%s,%s,%s)",
                       (u_name, u_name, u_pass))
        return render(request, 'index.html', {'Error': "New User Created Successfully"})
    else:
        return render(request, "index.html", {'Error': 'New User Creation Failed!! User Already Exists'})


def new_user(request):
    return render(request, 'new_user.html')


def set_default(request):
    global count, mark
    count = 10
    mark = 0
    return render(request, 'index.html')


def show_answer(ans, ack):
    global sub
    if ack:
        if_correct = "Selected Right Answer " + ans
        return if_correct
    else:
        if_wrong = "Oops, You are Wrong. Right Answer is " + ans
        return if_wrong


def answer_validate(request):
    global count, mark, sub
    selected = request.POST['option']
    if selected == correct:
        mark = mark + 1
        sub.append(show_answer(correct, True))
        return render(request, "quiz.html", {'ques_opt': sub, 'sub_val': 'hidden', 'nxt_val': ''})
    else:
        sub.append(show_answer(correct, False))
        return render(request, "quiz.html", {'ques_opt': sub, 'sub_val': 'hidden', 'nxt_val': ''})


def get_from_trivia():
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


def show_questions(request):
    global count, sub, mark
    if request.method == "GET" and count > 0:
        count = count - 1
        sub = []
        sub = get_from_trivia()
        return render(request, "quiz.html", {'ques_opt': sub, 'sub_val': '', 'nxt_val': 'hidden'})
    else:
        return render(request, "result.html", {'mark': mark})


def user_validate(request):
    if request.method == 'POST':
        uname = request.POST.get('uname', False)
        user_pass = request.POST.get('psw', False)
        cur = connection.cursor()
        cur.execute('select user_id,password from login_details where user_id=%s', [uname])
        results = cur.fetchall()
        if len(results) != 0:
            if str(uname) == str(results[0][0]) and str(user_pass) == str(results[0][1]):
                return render(request, "terms.html", {'Login': results[0],})
            else:
                return render(request, "index.html", {'Error': 'Invalid Login Details'})
        else:
            return render(request, "index.html", {'Error': 'Invalid Login Details'})
    else:
        return render(request, "index.html", {'Error': ''})