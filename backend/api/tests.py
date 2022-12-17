from django.test import TestCase
from api.models import *
from .utils import *
from course_picker.settings import BASE_DIR
import json


with open(str(BASE_DIR) + '/erkhes_otl.json') as fp:
    data = json.load(fp)
            
            
# Create your tests here.
class ParseUserTestCase(TestCase):
    def setUp(self):
        # Internally creates CPUser object
        parse_user(data)
    
    def test_user(self):
        erkhes = CPUser.objects.get(student_id=20190786)
        self.assertEqual(erkhes.major_type, None)
        self.assertEqual(erkhes.major, '')
        self.assertEqual(erkhes.minor, '')
        self.assertEqual(erkhes.first_name, 'Erkhes')
        self.assertEqual(erkhes.last_name, 'Nyamsaikhan')

class CSMajorRequiredTestCase(TestCase):
    def test(self):
        self.assertEqual("CS204" in get_cs_major_required(), True)
        self.assertEqual("CS206" in get_cs_major_required(), True)
        self.assertEqual("CS300" in get_cs_major_required(), True)
        self.assertEqual("CS311" in get_cs_major_required(), True)
        self.assertEqual("CS320" in get_cs_major_required(), True)
        self.assertEqual("CS330" in get_cs_major_required(), True)

class GetCurrentSemesterTestCase(TestCase):
    def test(self):
        self.assertEqual(get_current_semester(), (2022, 3))


class LectureListTestCase(TestCase):
    def setUp(self):
        parse_user(data)
        
    def test(self):
        erkhes = CPUser.objects.get(student_id=20190786)
        all_lectures = erkhes.lecture_list.lectures.all()
        # CS101 was taken before current semester
        self.assertEqual(all_lectures.filter(course__course_code='CS101').exists(), True)
        # CS350 is taken but Erkhes is taking it this semester
        self.assertEqual(all_lectures.filter(course__course_code='CS350').exists(), False)

class IsTakenTestCase(TestCase):
    def setUp(self):
        parse_user(data)
        
    def test(self):
        erkhes = CPUser.objects.get(student_id=20190786)
        self.assertEqual(is_taken_course(erkhes, 'CS101'), True)
        self.assertEqual(is_taken_course(erkhes, 'CS350'), False)

class RequirementTestCase(TestCase):
    def setUp(self):
        parse_user(data)
        erkhes = CPUser.objects.get(student_id=20190786)
        erkhes.major_type = False
        erkhes.major = 'CS'
        erkhes.minor = 'MAS'
        erkhes.save()
        
    def test(self):
        erkhes = CPUser.objects.get(student_id=20190786)
        self.assertEqual(get_requirement(erkhes)[0], 49) # CS major credits
        self.assertEqual(get_requirement(erkhes)[1], 19) # CS major required credits
        self.assertEqual(get_requirement(erkhes)[2], 18) # MAS minor credits

class OverlapTestCase(TestCase):
    def test(self):
        self.assertEqual(overlap((1, 10), (10, 15)), False) # overlap of intervals [1, 10], [10, 15]
        self.assertEqual(overlap((1, 10), (2, 11)), True) 
        self.assertEqual(overlap((1, 10), (2, 9)), True)

class GenerateSchedulesTestCase(TestCase):
    def setUp(self):
        parse_user(data)
    
    def test_schedules(self):
        erkhes = CPUser.objects.get(student_id=20190786)
        # Erkhes didn't take PH142, which is the one of the highest prioirity course in our system
        self.assertEqual(greedy_recommend(erkhes.student_id)[0]['old_code'], 'PH142')
        