from django.db import models

# Create your models here.

class Professor(models.Model):
    name=models.CharField(max_length=100) #professor name
    prof_id=models.IntegerField() #professor id
    review_total_weight=models.FloatField() #review total score of the professor



class Course(models.Model):
    title=models.CharField(max_length=200) # Introduction to Software Engineering
    # department_name=models.CharField(max_length=60)
    department_code=models.CharField(max_length=10)
    course_code=models.CharField(max_length=20)
    type=models.CharField(max_length=50)

# class Examtime(models.Model):
#     

class Lecture(models.Model):
    year=models.IntegerField()  #2022
    semester=models.IntegerField() #1: spring semester 3: fall semester
    num_classes=models.IntegerField() #hours of classes(lecture) ex) CS350 have 3hour of classes
    num_labs=models.IntegerField() #hours of labs ex) CS350 have 0hour of labs
    credit=models.IntegerField() #number of credit of the course
    credit_au=models.IntegerField() #number of AU of the course
    professor=models.ForeignKey(Professor, on_delete=models.CASCADE) #professor
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    review_total_weight=models.FloatField() #review total score of the lecture
    # courseGrade=models.IntegerField() #grade score of the lecture
    # courseLoad=models.IntegerField() #load score of the lecture
    # courseSpeech=models.IntegerField() #speech score of the lecture
    # classtime=models.ForeignKey(Timeslot, on_delete=models.CASCADE, related_name='classtime') #classtime ID
    # examtime=models.ForeignKey(Timeslot, on_delete=models.CASCADE, related_name="examtime") #examtime ID
   
class Time(models.Model):
    day=models.IntegerField() #class day: 0=Mon, 1=Tue, 2=Wen, 3=Thu, 4=Fri
    begin=models.IntegerField() #class beginning time: 720 -> 12:00PM 
    end=models.IntegerField() #class end time--> 810 -> 1:30PM
    lecture=models.ForeignKey(Lecture, on_delete=models.CASCADE)
        

class Examtime(models.Model):
    day=models.IntegerField() #exam day: 0=Mon, 1=Tue, 2=Wen, 3=Thu, 4=Fri
    begin=models.IntegerField() #exam beginning time: 1230--> 12pm 30min 
    end=models.IntegerField() #exam end time--> 1000--> 10am 0min
    lecture=models.ForeignKey(Lecture, on_delete=models.CASCADE)   
   
   
    
class LectureList(models.Model):
    lectures = models.ManyToManyField(Lecture)


class CPUser(models.Model):
    student_id=models.IntegerField() #ex)20220246
    major_type=models.BooleanField(null=True) # true: Double major, false: Major/minor
    major=models.CharField(max_length=5, default='') #CS: computer science, MAS: Mathematical, department_code
    minor=models.CharField(max_length=5, default='') #CS: computer science, MAS: Mathematical/ if isDual=false and secondMajor=MAS, user has MAS as a submajor
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # schedule_list=models.OneToOneField(
    #     ScheduleList,
    #     on_delete=models.CASCADE,
    #     primary_key=True
    # ) #schedulelist
    lecture_list=models.ForeignKey(LectureList, on_delete=models.CASCADE) #lecturelist
    
class Schedule(models.Model):
    user=models.ForeignKey(CPUser, on_delete=models.CASCADE)
    is_saved=models.BooleanField() #true: saved /false: nonsaved
    lecture_list=models.ForeignKey(LectureList, on_delete=models.CASCADE) #the list of lectures included in the schedule
    # scheduleRevTot=models.IntegerField() #review total score of the schedule
    # scheduleGrade=models.IntegerField() #grade score of the schedule
    # scheduleLoad =models.IntegerField() #load score of the schedule
    # scheduleSpeech=models.IntegerField() #speech score of the schedule