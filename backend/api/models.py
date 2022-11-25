from django.db import models

# Create your models here.
class CPUser(models.Model):
    studentID=models.IntegerField() #ex)20220246
    isDual=models.BooleanField() # true: Dual major, false: Sub major
    major=models.CharField(maxlength=5) #CS: computer science, MAS: Mathematical
    secondMajor=models.CharField(maxlength=5) #CS: computer science, MAS: Mathematical/ if isDual=false and secondMajor=MAS, user has MAS as a submajor
    scheduleList=models.ForeignKey(ScheduleList) #schedulelist
    lectureList=models.ForeignKey(LectureList) #lecturelist


class Lecture(models.Model):
    title=models.CharField(maxlength=5) # introduction to software engineering
    year=models.IntegerField()  #2022
    semester=models.IntegerField() #1: spring semester 2: fall semester
    departmentName=models.CharField() #CS
    # Limit=models.IntegerField() # the number of maximum students who can listen this course
    # isEng=models.BooleanField() # true: English is used in the course / false: korean will be used
    hourClasses=models.IntegerField() #hours of classes(lecture) ex) CS350 have 3hour of classes
    hourLabs=models.IntegerField() #hours of labs ex) CS350 have 0hour of labs
    credit=models.IntegerField() #number of credit of the course
    creditAU=models.IntegerField() #number of AU of the course
    professor=models.ForeignKey(Professor) #professor
    # courseRevTot=models.IntegerField() #review total score of the lecture
    # courseGrade=models.IntegerField() #grade score of the lecture
    # courseLoad=models.IntegerField() #load score of the lecture
    courseSpeech=models.IntegerField() #speech score of the lecture
    classTime=models.ForeignKey(Classtime) #classtime ID
    examTime=models.ForeignKey(Examtime) #examtime ID


class Schedule(models.Model):
    isSaved=models.BooleanField() #true: saved /false: nonsaved
    lectureList=models.ForeignKey(LectureList) #the list of lectures included in the schedule
    scheduleRevTot=models.IntegerField() #review total score of the schedule
    scheduleGrade=models.IntegerField() #grade score of the schedule
    scheduleLoad =models.IntegerField() #load score of the schedule
    scheduleSpeech=models.IntegerField() #speech score of the schedule


class Profrssor(models.Model):
    name=models.CharField(maxlength=100) #professor name
    profID=models.IntegerField() #professor id
    profRevTot=models.IntegerField() #review total score of the professor

class Classtime(models.Model):
    classbuildingName=models.CharField(maxlength=100) #class building name 
    classRoomName=models.CharField(maxlength=100) #class room name
    classRay=models.IntegerField() #class day: 1=Mon, 2=Tue, 3=Wen, 4=Thu, 5=Fri
    classBegin=models.IntegerField() #class beginning time: 1230--> 12pm 30min 
    classEnd=models.IntegerField() #class end time--> 1000--> 10am 0min

class Examtime(models.Model):
    examBuildingName=models.CharField(maxlength=100) #exam building name 
    examRoomName=models.CharField(maxlength=100) #exam room name
    examDay=models.IntegerField() #exam day: 1=Mon, 2=Tue, 3=Wen, 4=Thu, 5=Fri
    examBegin=models.IntegerField() #exam beginning time: 1230--> 12pm 30min 
    examEnd=models.IntegerField() #exam end time--> 1000--> 10am 0min


class ScheduleList(models.Model):



class LectureList(models.Model):




