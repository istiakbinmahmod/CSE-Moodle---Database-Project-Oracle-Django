from django.shortcuts import render, redirect
import random
import os
import hashlib
import datetime
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
# from .models import people
from django.db import connection
from django import template
# Create your views here.
from .loginOrSignUp import loginOrSignup
from .loginOrSignUp.loginOrSignup import user_logout


def home(request):
    result = None
    print('home e asi')
    try:
        cur = connection.cursor()
        cur.execute("select * from course")
        result = cur.fetchall()
        cur.close()
    except:
        print('product fetch failed')
        return redirect('/homepage')
    print('aso')
    dict_res = []
    for r in result:
        course_id = r[0]
        session_id = r[1]
        course_title = r[2]
        credit_hour = r[3]
        #print(course_id)
        #print(session_id)
        #print(credit_hour)
        #print(course_title)
        row = {'course_id':course_id, 'session_id':session_id, 'course_title':course_title, 'credit_hour': credit_hour}
        dict_res.append(row)
    cur.close()
    return render(request, 'homepage.html', {'courses':dict_res})

def profileadmincreatecourses(request):
    try:
        usr = request.session['username']
    except:
        user_logout(request)
    if request.method == 'POST':
        courseid = request.POST.get('courseid')
        sessionid = request.POST.get('sessionid')
        coursetitle = request.POST.get('coursetitle')
        credithour = request.POST.get('credithour')
        sql = "INSERT INTO COURSE(COURSE_ID, SESSION_ID, COURSE_TITLE, CREDIT_HOUR) VALUES(%s, %s, %s, %s)"
        try:
            cur = connection.cursor()
            cur.execute(sql, [courseid, sessionid, coursetitle, credithour])
            connection.commit()
            cur.close()
            return redirect('/home/profile/admin/createcourses')
        except:
            return redirect('/home/profile/admin/createcourses/')
    name = request.session['username']
    return render(request, 'create_courses.html', {'name': name})

def profileadminassignstucourses(request):

    try:
        usr = request.session['username']
    except:
        user_logout(request)
    if request.method == 'POST':
        profileid = request.POST.get('profileid')
        courseid = request.POST.get('courseid')
        sessionid = request.POST.get('sessionid')
        sql = "INSERT INTO STUDENTCOURSERELATION(PROFILE_ID, COURSE_ID, SESSION_ID) VALUES(%s, %s, %s)"
        try:
            cur = connection.cursor()
            cur.execute(sql, [profileid, courseid, sessionid])
            connection.commit()
            cur.close()
            return redirect('/home/profile/admin/assignstucourses')
        except:
            return redirect('/home/profile/admin/assignstucourses/')
    name = request.session['username']
    return render(request, 'assign_students_to_course.html', {'name': name})

def profileadminassignteacourses(request):
    try:
        usr = request.session['username']
    except:
        user_logout(request)
    if request.method == 'POST':
        profileid = request.POST.get('profileid')
        courseid = request.POST.get('courseid')
        sessionid = request.POST.get('sessionid')
        sql = "INSERT INTO INSTRUCTORCOURSERELATION(PROFILE_ID, COURSE_ID, SESSION_ID) VALUES(%s, %s, %s)"
        try:
            cur = connection.cursor()
            cur.execute(sql, [profileid, courseid, sessionid])
            print(profileid)
            print(courseid)
            print(sessionid)
            connection.commit()
            cur.close()
            return redirect('/home/profile/admin/assignteacourses')
        except:
            return redirect('/home/profile/admin/assignteacourses/')
    name = request.session['username']
    return render(request, 'assign_teachers_to_course.html', {'name': name})


def studentcourse(request):
    return render(request, 'studentcourse.html', {'courseid':request.session['usercourseid'], 'sessionid':request.session['usersessionid']})

def teachercourse(request):
    return render(request, 'teachercourse.html', {'courseid':'CSEEEEE', 'sessionid':'21555'})