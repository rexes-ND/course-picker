import datetime
import pytz
import requests
import json
from api.models import *

def get_current_semester():
    return (2022, 3)

CSnext={"CS204":["CS300"], "CS206":["CS300","CS360"],"CS220":[],
"CS230":["CS311","CS320","CS330"],"CS270":[],"CS300":[],
"CS311":[],"CS320":[],"CS330":[],"CS341":[],"CS348":[],"CS350":[],"CS360":[],
"CS372":[],"CS374":[],"CS376":[],"CS380":[],"CS402":[],"CS408":[],"CS409":[],
"CS420":[],"CS422":[],"CS431":[],"CS442":[],"CS443":[],"CS453":[],"CS454":[],
"CS457":[],"CS458":[],"CS459":[],"CS470":[],"CS473":[],"CS474":[],"CS475":[],
"CS482":[],"CS484":[],"CS489":[],"CS492":[]}

CSpre={"CS204":[], "CS206":[],"CS220":[],"CS230":[],"CS270":[],"CS300":["CS204","CS206"],
"CS311":["CS230"],"CS320":["CS230"],"CS330":["CS230"],"CS341":[],"CS348":[],"CS350":[],"CS360":["CS206"],
"CS372":[],"CS374":[],"CS376":[],"CS380":[],"CS402":[],"CS408":[],"CS409":[],
"CS420":[],"CS422":[],"CS431":[],"CS442":[],"CS443":[],"CS453":[],"CS454":[],
"CS457":[],"CS458":[],"CS459":[],"CS470":[],"CS473":[],"CS474":[],"CS475":[],
"CS482":[],"CS484":[],"CS489":[],"CS492":[]}

MASnext={"MAS210":["MAS410"],"MAS212":["MAS410","MAS435","MAS370"],"MAS241":["MAS242","MAS341"],"MAS242":["MAS440","MAS441","MAS443"],"MAS260":[],"MAS270":[],"MAS275":["MAS477","MAS478"],
"MAS311":["MAS312","MAS370","MAS435"],"MAS312":["MAS410","MAS411"],"MAS321":[],"MAS331":["MAS435"],"MAS341":[],"MAS350":[],"MAS355":[],"MAS364":[],
"MAS365":[],"MAS370":[],"MAS374":[],"MAS410":[],"MAS411":[],"MAS420":[],"MAS430":[],
"MAS435":[],"MAS440":[],"MAS441":[],"MAS442":[],"MAS443":[],"MAS456":[],"MAS464":[],
"MAS471":[],"MAS476":[],"MAS477":[],"MAS478":[]}

MASpre={"MAS210":[],"MAS212":[],"MAS241":[],"MAS242":["MAS241"],"MAS260":[],"MAS270":[],"MAS275":[],
"MAS311":[],"MAS312":["MAS311"],"MAS321":[],"MAS331":[],"MAS341":["MAS241"],"MAS350":[],"MAS355":[],"MAS364":[],
"MAS365":[],"MAS370":["MAS212","MAS311"],"MAS374":[],"MAS410":["MAS210","MAS212","MAS312"],"MAS411":["MAS312"],"MAS420":[],"MAS430":[],
"MAS435":["MAS212","MAS311","MAS331"],"MAS440":["MAS242"],"MAS441":["MAS242"],"MAS442":[],"MAS443":["MAS242"],"MAS456":[],"MAS464":[],
"MAS471":[],"MAS476":[],"MAS477":["MAS275"],"MAS478":["MAS275"]}

def get_cs_major_required():
    return [
        "CS204", "CS206", "CS300",
        "CS311", "CS320", "CS330"
    ]

def get_basic_required():
    return [
        "CS101", "MAS101", "MAS102", "BS120", 
        "CH101", "CH102", "PH141", "PH151", "PH142"
    ]

def parse_user(data):
    student_id = int(data['student_id'])
    first_name = data['firstName']
    last_name=data['lastName']
    lecture_list=LectureList.objects.create()
    
    review_writable_lectures = data['review_writable_lectures']
    for rwl in review_writable_lectures:
        if ((rwl['year'], rwl['semester']) == get_current_semester()):
            continue
        prof = rwl['professors'][0]
        professor, _ = Professor.objects.get_or_create(name=prof['name_en'], prof_id=prof['professor_id'], review_total_weight=prof['review_total_weight'])
        course, _ = Course.objects.get_or_create(title=rwl['common_title_en'], department_code=rwl['department_code'], course_code=rwl['old_code'], type=rwl['type_en'])
        lecture, _  = Lecture.objects.get_or_create(
            year=rwl['year'], 
            semester=rwl['semester'], 
            num_classes=rwl['num_classes'],
            num_labs=rwl['num_labs'],
            credit=rwl['credit'],
            credit_au=rwl['credit_au'],
            professor=professor,
            course=course,
            review_total_weight=rwl['review_total_weight']
        )
        if (len(rwl['classtimes']) > 0):
            for ct in rwl['classtimes']:
                Time.objects.get_or_create(day=ct['day'], begin=ct['begin'], end=ct['end'], lecture=lecture)
        if (len(rwl['examtimes']) > 0):
            for et in rwl['examtimes']:
                Examtime.objects.get_or_create(day=et['day'], begin=et['begin'], end=et['end'], lecture=lecture)
        
        lecture_list.lectures.add(lecture)
    user, _ = CPUser.objects.get_or_create(
        student_id=student_id, 
        first_name=first_name,
        last_name=last_name,
        lecture_list=lecture_list
    )
    return user

def get_requirement(user): # -> (CS, CSR, MAS, HSS)
    # user = CPUser.objects.get(student_id=student_id)
    if (user.major_type): # Double major
        if (user.major == "CS"):
            # user.minor == "MAS"
            return (49, 19, 40, 19)
        else:
            # user.major == "MAS"
            return (40, 19, 42, 19)
    else: # Major/minor
        if (user.major == "CS"):
            return (49, 19, 18, 28)
        else:
            return (21, 15, 42, 28)

def is_taken_course(user: CPUser, course_code):
    l = user.lecture_list.lectures.all().filter(course__course_code=course_code)
    if (len(l) == 0):
        return False
    return True

def get_user_stat(user: CPUser):
    lectures = user.lecture_list.lectures.all()
    cs_major_required_credits = 0
    cs_major_required_courses_taken = []
    cs_major_credits = 0
    cs_major_courses_taken = []
    mas_major_credits = 0
    mas_major_courses_taken = []
    hss_credits = 0
    hss_courses_taken = []
    basic_required_credits = 0
    basic_required_courses_taken = []
    cs_major_required_courses = get_cs_major_required()
    basic_required_courses = get_basic_required()
    common_be = ["MAS250", "MAS109"]
    for l in lectures:
        if (l.course.course_code in basic_required_courses):
            basic_required_credits += l.credit
            basic_required_courses_taken.append(l.course.course_code)
            continue
        if (l.course.course_code in cs_major_required_courses):
            cs_major_required_credits += l.credit
            cs_major_required_courses_taken.append(l.course.course_code)
        if (l.course.department_code == "CS"):
            cs_major_credits += l.credit
            cs_major_courses_taken.append(l.course.course_code)
        if (l.course.department_code == "MAS" and l.course.course_code not in common_be):
            mas_major_credits += l.credit
            mas_major_courses_taken.append(l.course.course_code)
        if (l.course.department_code == "HSS"):
            hss_credits += l.credit
            hss_courses_taken.append(l.course.course_code)
    return {
        "cs_major_required_credits": cs_major_required_credits,
        "cs_major_required_courses_taken": cs_major_required_courses_taken,
        "cs_major_credits": cs_major_credits,
        "cs_major_courses_taken": cs_major_courses_taken,
        "mas_major_credits": mas_major_credits,
        "mas_major_courses_taken": mas_major_courses_taken,
        "hss_credits": hss_credits,
        "hss_courses_taken": hss_courses_taken,
        "basic_required_credits": basic_required_credits,
        "basic_required_courses_taken": basic_required_courses_taken,
    } 
        
def overlap(t1, t2):
    if (t1[0] <= t2[0]):
        if (t1[1] <= t2[0]):
            return False
        else:
            return True
    else:
        if (t2[1] <= t1[0]):
            return False
        else:
            return True      

def get_score(user, course, stat):
    cs_must, csr_must, mas_must, hss_must = get_requirement(user)
    # Return low score for course the user have already taken
    score = 0
    if is_taken_course(user, course['old_code']):
        return -1
    if course['old_code'] in stat['cs_major_required_courses_taken']:
        return -1
    if course['old_code'] in stat['cs_major_courses_taken']:
        return -1
    if course['old_code'] in stat['mas_major_courses_taken']:
        return -1
    if course['old_code'] in stat['hss_courses_taken']:
        return -1
    if course['old_code'] in stat['basic_required_courses_taken']:
        return -1
    course_picked = stat['course_picked']
    for cp in course_picked:
        for classtime in cp['classtimes']:
            for course_classtime in course['classtimes']:
                if (classtime['day'] == course_classtime['day'] and overlap((classtime['begin'], classtime['end']),(course_classtime['begin'], course_classtime['end']))):
                    return -1
    # stat = get_user_stat(user)
    br = get_basic_required()
    csr = get_cs_major_required()
    csr_fulfilled = False
    cs_fulfilled = False
    mas_fulfilled = False
    if (course['old_code'] in br):
        return 100
    if (course['department_code'] == user.major):
        score += 50
    if (stat['cs_major_required_credits'] < csr_must and course['old_code'] in csr):
        score += 10
    elif (stat['cs_major_required_credits'] >= csr_must):
        csr_fulfilled = True
    if (stat['cs_major_credits'] < cs_must and course['department_code'] == "CS" and int(course['old_code'][2:]) <= 490):
        score += 10
    elif (stat['cs_major_credits'] >= cs_must):
        cs_fulfilled = True
    if (stat['mas_major_credits'] < mas_must and course['department_code'] == "MAS" and int(course['old_code'][3:]) <= 490):
        score += 20
        if (cs_fulfilled and csr_fulfilled):
            score += 50
    elif (stat['mas_major_credits'] >= mas_must):
        mas_fulfilled = True
    if (stat['hss_credits'] < hss_must and course['department_code'] == "HSS" and int(course['old_code'][3:]) <= 490):
        score += 10
        if (csr_fulfilled and cs_fulfilled and mas_fulfilled):
            score += 50
    # if (course['old_code'] == 'MAS242'):
    #     print(score)
    return score
    


def greedy_recommend(student_id):
    user = CPUser.objects.get(student_id=student_id)
    cur_year, cur_month = get_current_semester()
    stat = get_user_stat(user)
    all_courses = []
    r = requests.get("https://otl.kaist.ac.kr/api/lectures?year={}&semester={}&group=CS".format(cur_year, cur_month))
    cs_json = json.loads(r.text)
    all_courses.extend(cs_json)
    r = requests.get("https://otl.kaist.ac.kr/api/lectures?year={}&semester={}&department=MAS&type=ME".format(cur_year, cur_month))
    mas_json = json.loads(r.text)
    all_courses.extend(mas_json)
    r = requests.get("https://otl.kaist.ac.kr/api/lectures?year={}&semester={}&group=Humanity".format(cur_year, cur_month))
    hss_json = json.loads(r.text)
    all_courses.extend(hss_json)
    r = requests.get("https://otl.kaist.ac.kr/api/lectures?year={}&semester={}&type=BR".format(cur_year, cur_month))
    br_json = json.loads(r.text)
    all_courses.extend(br_json)
    course_picked = []
    stat['course_picked'] = course_picked
    for i in range(5):
        def sorting_function(course):
            return get_score(user, course, stat)
        all_courses.sort(key=sorting_function, reverse=True)
        course_picked.append(all_courses[0])
        if all_courses[0]['old_code'] in get_basic_required():
            stat['basic_required_credits'] += all_courses[0]['credit']
            stat['basic_required_courses_taken'].append(all_courses[0]['old_code'])
        if all_courses[0]['old_code'] in get_cs_major_required():
            stat['cs_major_required_credits'] += all_courses[0]['credit']
            stat['cs_major_required_courses_taken'].append(all_courses[0]['old_code'])
        if all_courses[0]['department_code'] == 'CS':
            stat['cs_major_credits'] += all_courses[0]['credit']
            stat['cs_major_courses_taken'].append(all_courses[0]['old_code'])
        if all_courses[0]['department_code'] == 'MAS':
            stat['mas_major_credits'] += all_courses[0]['credit']
            stat['mas_major_courses_taken'].append(all_courses[0]['old_code'])
        if all_courses[0]['department_code'] == 'HSS':
            stat['hss_credits'] += all_courses[0]['credit']
            stat['hss_courses_taken'].append(all_courses[0]['old_code'])
        stat['course_picked'] = course_picked
        # print(stat)
    return course_picked    
            





