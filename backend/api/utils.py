import datetime
import pytz
from api.models import *

def get_current_semester():
    return (2022, 3)


def parse_user(data):
    student_id = int(data['student_id'])
    first_name = data['firstName']
    last_name=data['lastName']
    lecture_list=LectureList.objects.create()
    
    review_writable_lectures = data['review_writable_lectures']
    for rwl in review_writable_lectures:
        print("rwl")
        prof = rwl['professors'][0]
        professor, _ = Professor.objects.get_or_create(name=prof['name_en'], prof_id=prof['professor_id'], review_total_weight=prof['review_total_weight'])
        course, _ = Course.objects.get_or_create(title=rwl['common_title_en'], department_code=rwl['department_code'], course_code=rwl['old_code'])
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