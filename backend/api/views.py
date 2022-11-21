from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.backends.db import SessionStore
import requests
import json
from urllib import parse
from bs4 import BeautifulSoup

def index(request):
    return JsonResponse({
        "status": 200,
        "msg": "You are at index"
    })


def login_handler(request):

    s = requests.Session()
    otl_header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    print("START - https://otl.kaist.ac.kr/session/login/?next=https://otl.kaist.ac.kr/")
    r = s.get("https://otl.kaist.ac.kr/session/login/?next=https://otl.kaist.ac.kr/", headers = otl_header, allow_redirects=False)
    otl_sessionid = r.cookies['sessionid']
    print("OTL SESSION ID:",otl_sessionid)
    print("FINISH - https://otl.kaist.ac.kr/session/login/?next=https://otl.kaist.ac.kr/")
    
    sso_header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "Referer": "https://otl.kaist.ac.kr/",
        # "Host": "sparcssso.kaist.ac.kr"
    }
    cur_url = r.headers['Location']
    print("START -", cur_url) # https://sparcssso.kaist.ac.kr/api/v2/token/require/?client_id=otlplus&state=f84527fdc9eeaa3ba2d9
    r = s.get(r.headers['Location'], headers=sso_header, allow_redirects=False)
    print("FINISH -", cur_url)
    
    cur_url = "https://sparcssso.kaist.ac.kr" + r.headers['Location']
    print("START -", cur_url)
    sso_header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    r = s.get(cur_url, headers=sso_header, allow_redirects=False)
    # print(r.text)
    sso_sessionid = r.cookies['sessionid']
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf_token = soup.find('input')['value']
    
    print('SSO SESSION ID:',sso_sessionid)
    print("FINISH -", cur_url)
    #
    print("START =", "https://sparcssso.kaist.ac.kr/account/login/kaist/")
    sso_header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "Referer": cur_url, # https://sparcssso.kaist.ac.kr/account/login/?next=/api/v2/token/require/?client_id=otlplus&state=f84527fdc9eeaa3ba2d9
        "Content-Type": "application/x-www-form-urlencoded"
    }
    r = s.post("https://sparcssso.kaist.ac.kr/account/login/kaist/", headers=sso_header, data={"csrfmiddlewaretoken": csrf_token}, allow_redirects=False)
    print("FINISH =", "https://sparcssso.kaist.ac.kr/account/login/kaist/")
    
    cur_url = r.headers['Location'] # https://iam2.kaist.ac.kr/api/sso/commonLogin?client_id=SPARCS&state=8cd39f1d-64d1-46c7-a047-191d1505e0ef&redirect_url=https%3A%2F%2Fsparcssso.kaist.ac.kr%2Faccount%2Fcallback%2F
    
    cur_url = cur_url.replace("https%3A%2F%2Fsparcssso.kaist.ac.kr%2Faccount%2Fcallback%2F", "http%3A%2F%2Flocalhost%3A8001%2Fapi%2Fv1%2Fauth%2Fcallback%2F")
    cur_url += request.session.session_key
    request.session['sso_sessionid'] = sso_sessionid
    request.session['otl_sessionid'] = otl_sessionid
    print("REDIRECTING TO",cur_url)
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
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    sso_cookie = {
        "sessionid": sso_sessionid
    }
    session = requests.Session()
    print("START - https://sparcssso.kaist.ac.kr/account/callback/")
    r = session.post("https://sparcssso.kaist.ac.kr/account/callback/", headers=sso_header, cookies=sso_cookie, data=request.body, allow_redirects=False)
    print(r.request.headers)
    print(r.headers)
    print("FINISH - https://sparcssso.kaist.ac.kr/account/callback/")
    sso_header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    cur_url = "https://sparcssso.kaist.ac.kr"+r.headers['Location']
    print("START -", cur_url)
    r = session.get(cur_url, headers=sso_header, allow_redirects=False)
    print(r.request.headers)
    print(r.headers)
    print("FINISH -", cur_url)
    cur_url = r.headers['Location']
    otl_header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    otl_cookie = {
        "sessionid": otl_sessionid
    }
    print("START -", cur_url)
    r = session.get(cur_url, headers=otl_header, cookies=otl_cookie, allow_redirects=False)
    print(r.headers)
    print("FINISH -", cur_url)
    r = session.get("https://otl.kaist.ac.kr/session/info")
    print(r.text)
    # request_url
    return JsonResponse(
        json.loads(r.text)
    )
    