from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.backends.db import SessionStore
from api.models import CPUser, LectureList
from .utils import parse_user
import requests
import json
from urllib import parse
from bs4 import BeautifulSoup

frontend_url = "http://localhost:3000"
otl_url = "https://otl.kaist.ac.kr"
sparcssso_url = "https://sparcssso.kaist.ac.kr"
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
def index(request):
    return JsonResponse({
        "status": 200,
        "msg": "You are at index",
        "sessionid": request.session.session_key
    })
@csrf_exempt 
def login_status(request):
    # print(request.session.session_key)
    # print(request.session.get('otl_sessionid', ""))
    r = requests.get(otl_url+"/session/info", cookies = {"sessionid": request.session.get('otl_sessionid')})
    if (r.status_code == 200):
        return JsonResponse({
            "status": 200,
        })
    return JsonResponse({
        "status": 401
    })
@csrf_exempt
def logout_handler(request):
    del request.session
    s = SessionStore()
    s.create()
    res = JsonResponse({
        "status": 200
    })
    request.session = s
    return redirect(frontend_url+"/login")
def login_handler(request):
    s = requests.Session()
    otl_header = {
        "User-Agent": user_agent
    }
    r = s.get(otl_url+"/session/login/?next="+otl_url+"/", headers = otl_header, allow_redirects=False)
    otl_sessionid = r.cookies['sessionid']
    
    sso_header = {
        "User-Agent": user_agent,
        "Referer": otl_url+"/",
        # "Host": "sparcssso.kaist.ac.kr"
    }
    cur_url = r.headers['Location']
    r = s.get(r.headers['Location'], headers=sso_header, allow_redirects=False)
    
    cur_url = sparcssso_url + r.headers['Location']
    sso_header = {
        "User-Agent": user_agent 
    }
    r = s.get(cur_url, headers=sso_header, allow_redirects=False)
    # print(r.text)
    sso_sessionid = r.cookies['sessionid']
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf_token = soup.find('input')['value']
    
    sso_header = {
        "User-Agent": user_agent,
        "Referer": cur_url, # https://sparcssso.kaist.ac.kr/account/login/?next=/api/v2/token/require/?client_id=otlplus&state=f84527fdc9eeaa3ba2d9
        "Content-Type": "application/x-www-form-urlencoded"
    }
    r = s.post(sparcssso_url+"/account/login/kaist/", headers=sso_header, data={"csrfmiddlewaretoken": csrf_token}, allow_redirects=False)
    
    cur_url = r.headers['Location'] # https://iam2.kaist.ac.kr/api/sso/commonLogin?client_id=SPARCS&state=8cd39f1d-64d1-46c7-a047-191d1505e0ef&redirect_url=https%3A%2F%2Fsparcssso.kaist.ac.kr%2Faccount%2Fcallback%2F
    
    cur_url = cur_url.replace("https%3A%2F%2Fsparcssso.kaist.ac.kr%2Faccount%2Fcallback%2F", "http%3A%2F%2Flocalhost%3A8001%2Fapi%2Fv1%2Fauth%2Fcallback%2F")
    if not request.session.session_key:
        request.session.save()
    cur_url += request.session.session_key
    request.session['sso_sessionid'] = sso_sessionid
    request.session['otl_sessionid'] = otl_sessionid
    # print(request.)
    return redirect(cur_url)

@csrf_exempt    
def callback_handler(request, sessionid):
    s = SessionStore(session_key=sessionid)
    sso_sessionid = s['sso_sessionid']
    otl_sessionid = s['otl_sessionid']
    sso_header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://iam2.kaist.ac.kr/",
        "User-Agent": user_agent
    }
    sso_cookie = {
        "sessionid": sso_sessionid
    }
    session = requests.Session()
    r = session.post(sparcssso_url+"/account/callback/", headers=sso_header, cookies=sso_cookie, data=request.body, allow_redirects=False)
    sso_header = {
        "User-Agent": user_agent 
    }
    cur_url = sparcssso_url+r.headers['Location']
    r = session.get(cur_url, headers=sso_header, allow_redirects=False)
    cur_url = r.headers['Location']
    otl_header = {
        "User-Agent": user_agent
    }
    otl_cookie = {
        "sessionid": otl_sessionid
    }
    r = session.get(cur_url, headers=otl_header, cookies=otl_cookie, allow_redirects=False)
    r = session.get(otl_url+"/session/info")
    s["otl_sessionid"] = session.cookies.get_dict(domain="otl.kaist.ac.kr")['sessionid']
    r_json = json.loads(r.text)
    print(r_json)
    student_id = int(r_json['student_id'])
    try:
        user = CPUser.objects.get(student_id=student_id)
    except CPUser.DoesNotExist:
        # lecture_list=LectureList.objects.create()
        # user = CPUser.objects.create(student_id=student_id, first_name=r_json['firstName'], last_name=r_json['lastName'], lecture_list=lecture_list)
        user = parse_user(r_json)
    # if (user_is_created):
    #     print("User is created")
    # else:
    #     print("User is already created") 
    s["student_id"] = student_id
    s.save()
    res = redirect(frontend_url)
    # print("PRINTING SESSION ID BEFORE REDIRECTING",request.session.session_key)
    # res.cookies['sessionid'] = request.session.session_key
    return res

def current_user(request):
    student_id = request.session.get('student_id')
    if (student_id is None):
        return JsonResponse({
            "status": 404
        })
    user = CPUser.objects.get(student_id=student_id)
    return JsonResponse({
        "status": 200,
        "student_id": student_id,
        "major_type": user.major_type,
        "major": user.major,
        "minor": user.minor,
        "first_name": user.first_name,
        "last_name": user.last_name,
    })

@csrf_exempt
def update_user(request):
    student_id = request.session.get('student_id')
    if (student_id is None):
        return JsonResponse({
            "status": 404
        })
    user = CPUser.objects.get(student_id=student_id)
    body_json = json.loads(request.body)
    # print(json.loads(request.body)) #{'majorType': False, 'major': 'CS', 'minor': 'MAS'}
    user.major_type = body_json['majorType']
    user.major = body_json['major']
    user.minor = body_json['minor']
    user.save()
    return JsonResponse({
        "status": 200,
    })
