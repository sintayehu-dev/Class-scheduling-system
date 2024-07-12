from django.db import models
import math
import random as rnd
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete
from datetime import timedelta, date

time_slots = (
    ('2:00 - 4:00', '2:00 - 4:00'),
    ('4:00 - 6:00', '4:00 - 6:00'),
    ('8:00 - 10:00', '8:00 - 10:00'), 
)

DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
)

BATCH = (
    ('G2', 'G2'),
    ('G3', 'G3'),
    ('G4', 'G4'),
    ('G5', 'G5'),
)

DEPARTMENT = (
    ('CS', 'CS'),
    ('IT', 'IT'),
    ('SE', 'SE'),
)

POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1


class Room(models.Model):
    r_number = models.CharField(max_length=6)
    seating_capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.r_number


class Instructor(models.Model):
    uid = models.CharField(max_length=6)
    name = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.uid} {self.name}'


class MeetingTime(models.Model):
    pid = models.CharField(max_length=4, primary_key=True)
    time = models.CharField(max_length=50, choices=time_slots, default='2:00 - 4:00')
    day = models.CharField(max_length=15, choices=DAYS_OF_WEEK)

    def __str__(self):
        return f'{self.pid} {self.day} {self.time}'
    
    def get_day_sort_key(self):
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        times_order = ['2:00 - 4:00', '4:00 - 6:00', '8:00 - 10:00']  # Define the order of time slots
        
        # Get index for day and time
        day_index = days_order.index(self.day)
        time_index = times_order.index(self.time)
        
        # Return a tuple that combines day and time index
        return (day_index, time_index)


class Course(models.Model):
    course_number = models.CharField(max_length=5, primary_key=True)
    course_name = models.CharField(max_length=40)
    max_numb_students = models.CharField(max_length=65)
    instructors = models.ManyToManyField(Instructor)

    def __str__(self):
        return f'{self.course_number} {self.course_name}'


class Department(models.Model):
    dept_name = models.CharField(max_length=50)

    def __str__(self):
        return self.dept_name


class Batch(models.Model):
    batch_name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)  # Associate courses with batches
      
    @property
    def get_courses(self):
        return self.courses

    def __str__(self):
        return self.batch_name


class Section(models.Model):
    section_id = models.CharField(max_length=25, primary_key=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    num_class_in_week = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    meeting_time = models.ForeignKey(MeetingTime, on_delete=models.CASCADE, blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, blank=True, null=True)

    def set_room(self, room):
        section = Section.objects.get(pk=self.section_id)
        section.room = room
        section.save()

    def set_meetingTime(self, meetingTime):
        section = Section.objects.get(pk=self.section_id)
        section.meeting_time = meetingTime
        section.save()

    def set_instructor(self, instructor):
        section = Section.objects.get(pk=self.section_id)
        section.instructor = instructor
        section.save()


class TimeTableModel(models.Model):
    section = models.CharField(max_length=100)
    batch = models.CharField(max_length=100)  # Update to use batch
    course = models.CharField(max_length=50)
    venue = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    clstime = models.CharField(max_length=100)
class PDF(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='pdfs/')

    def str(self):
        return self.title