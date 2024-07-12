from django.http import request, HttpResponse
from django.shortcuts import render, redirect
from . forms import *
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .render import Render
from django.views.generic import View
from django.template import loader


POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.05

class Data:
    def __init__(self):
        self._rooms = Room.objects.all()
        self._meetingTimes = MeetingTime.objects.all()
        self._instructors = Instructor.objects.all()
        self._courses = Course.objects.all()
        self._depts = Department.objects.all()
        self._batches = Batch.objects.all()  # Add this line to include batches

    def get_rooms(self): return self._rooms
    def get_instructors(self): return self._instructors
    def get_courses(self): return self._courses
    def get_depts(self): return self._depts
    def get_meetingTimes(self): return self._meetingTimes
    def get_batches(self): return self._batches  # Add this method to retrieve batches



class Schedule:
    def __init__(self):
        self._data = data
        self._classes = []
        self._numberOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True

    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes

    def get_numbOfConflicts(self): return self._numberOfConflicts

    def get_fitness(self):
        if self._isFitnessChanged:
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness

    def initialize(self):
        sections = Section.objects.all()
        for section in sections:
            batch = section.batch
            courses = batch.courses.all()
            for course in courses:
                for i in range(section.num_class_in_week // len(courses)):
                    newClass = Class(self._classNumb, batch.department, section.section_id, course, batch)
                    self._classNumb += 1
                    newClass.set_meetingTime(data.get_meetingTimes()[rnd.randrange(0, len(data.get_meetingTimes()))])
                    newClass.set_room(data.get_rooms()[rnd.randrange(0, len(data.get_rooms()))])
                    newClass.set_instructor(course.instructors.all()[rnd.randrange(0, len(course.instructors.all()))])
                    self._classes.append(newClass)
        return self

    def calculate_fitness(self):
        self._numberOfConflicts = 0
        classes = self.get_classes()
        for i in range(len(classes)):
            if classes[i].room.seating_capacity < int(classes[i].course.max_numb_students):
                self._numberOfConflicts += 1
            for j in range(len(classes)):
                if j >= i:
                    if (classes[i].meeting_time == classes[j].meeting_time) and \
                            (classes[i].section_id != classes[j].section_id):
                        if classes[i].room == classes[j].room:
                            self._numberOfConflicts += 1
                        if classes[i].instructor == classes[j].instructor:
                            self._numberOfConflicts += 1
        return 1 / (1.0 * self._numberOfConflicts + 1)



class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = [Schedule().initialize() for i in range(size)]

    def get_schedules(self):
        return self._schedules


class GeneticAlgorithm:
    def evolve(self, population):
        return self._mutate_population(self._crossover_population(population))

    def _crossover_population(self, pop):
        crossover_pop = Population(0)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop

    def _mutate_population(self, population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population

    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule().initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if rnd.random() > 0.5:
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule

    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule().initialize()
        for i in range(len(mutateSchedule.get_classes())):
            if MUTATION_RATE > rnd.random():
                mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule

    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop


class Class:
    def __init__(self, id, dept, section, course, batch):
        self.section_id = id
        self.department = dept
        self.course = course
        self.instructor = None
        self.meeting_time = None
        self.room = None
        self.section = section
        self.batch = batch  #Add batch to the class

    def get_id(self): return self.section_id
    def get_dept(self): return self.department
    def get_course(self): return self.course
    def get_instructor(self): return self.instructor
    def get_meetingTime(self): return self.meeting_time
    def get_room(self): return self.room
    def get_batch(self): return self.batch  #Add getter for batch

    def set_instructor(self, instructor): self.instructor = instructor
    def set_meetingTime(self, meetingTime): self.meeting_time = meetingTime
    def set_room(self, room): self.room = room


data = Data()


def context_manager(schedule):
    classes = schedule.get_classes()
    context = []
    for cls in classes:
        context.append({
            "section": cls.section_id,
            "dept": cls.department.dept_name,
            "course": f'{cls.course.course_name} ({cls.course.course_number}, {cls.course.max_numb_students})',
            "room": f'{cls.room.r_number} ({cls.room.seating_capacity})',
            "instructor": f'{cls.instructor.name} ({cls.instructor.uid})',
            "meeting_time": [cls.meeting_time.pid, cls.meeting_time.day, cls.meeting_time.time],
            "batch": cls.batch.batch_name  # Add batch to the context
        })
    return context

def timetable(request):
    population = Population(POPULATION_SIZE)
    generation_num = 0
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    geneticAlgorithm = GeneticAlgorithm()
    TimeTableModel.objects.all().delete()

    while population.get_schedules()[0].get_fitness() != 1.0:
        generation_num += 1
        print('\n> Generation #' + str(generation_num))
        population = geneticAlgorithm.evolve(population)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    
    schedule = population.get_schedules()[0].get_classes()

    # Debugging: Check if any meeting_time is None
    for cls in schedule:
        if cls.meeting_time is None:
            print(f"Error: meeting_time is None for class {cls}")

    # Sort the schedule by day and time
    schedule.sort(key=lambda cls: cls.meeting_time.get_day_sort_key())

    for sec in Section.objects.all():
        for scd in schedule:
            if scd.section == sec.section_id:
                t = TimeTableModel.objects.create()
                t.section = str(sec.section_id)
                t.batch = str(sec.batch.batch_name)  # Update to save batch
                t.course = str(scd.course)
                t.venue = str(scd.room)
                t.instructor = str(scd.instructor.name)
                t.clstime = str(scd.meeting_time)
                t.save()

    return render(request, 'gentimetable.html', {'schedule': schedule, 'sections': Section.objects.all(), 'times': MeetingTime.objects.all()})


############################################################################

def index(request):
    return render(request, 'index.html', {})


def aboutus(request):
    return render(request, 'aboutus.html', {})


def edittt(request):
    return render(request, 'edittimetable.html',{})

def help(request):
    return render(request, 'help.html', {})


def terms(request):
    return render(request, 'terms.html', {})


#################################################################################

@login_required
def admindash(request):
    return render(request, 'admindashboard.html', {})

#################################################################################

@login_required
def addCourses(request):
    form = CourseForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('addCourses')
        else:
            print('Invalid')
    context = {
        'form': form
    }
    return render(request, 'addCourses.html', context)

@login_required
def course_list_view(request):
    context = {
        'courses': Course.objects.all()
    }
    return render(request, 'courseslist.html', context)

@login_required
def delete_course(request, pk):
    crs = Course.objects.filter(pk=pk)
    if request.method == 'POST':
        crs.delete()
        return redirect('editcourse')

#################################################################################

@login_required
def addInstructor(request):
    if request.method == 'POST':
        form = InstructorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addInstructors')
    else:
        form = InstructorForm()

    context = {
        'form': form
    }
    return render(request, 'addInstructors.html', context)

@login_required
def inst_list_view(request):
    context = {
        'instructors': Instructor.objects.all()
    }
    return render(request, 'inslist.html', context)

@login_required
def delete_instructor(request, pk):
    inst = Instructor.objects.filter(pk=pk)
    if request.method == 'POST':
        inst.delete()
        return redirect('editinstructor')

#################################################################################

@login_required
def addRooms(request):
    form = RoomForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('addRooms')
    context = {
        'form': form
    }
    return render(request, 'addRooms.html', context)

@login_required
def room_list(request):
    context = {
        'rooms': Room.objects.all()
    }
    return render(request, 'roomslist.html', context)

@login_required
def delete_room(request, pk):
    rm = Room.objects.filter(pk=pk)
    if request.method == 'POST':
        rm.delete()
        return redirect('editrooms')

#################################################################################

@login_required
def addTimings(request):
    form = MeetingTimeForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('addTimings')
        else:
            print('Invalid')
    context = {
        'form': form
    }
    return render(request, 'addTimings.html', context)

@login_required
def meeting_list_view(request):
    context = {
        'meeting_times': MeetingTime.objects.all()
    }
    return render(request, 'mtlist.html', context)

@login_required
def delete_meeting_time(request, pk):
    mt = MeetingTime.objects.filter(pk=pk)
    if request.method == 'POST':
        mt.delete()
        return redirect('editmeetingtime')

#################################################################################

@login_required
def addDepts(request):
    form = DepartmentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('addDepts')
    context = {
        'form': form
    }
    return render(request, 'addDepts.html', context)


@login_required
def department_list(request):
    context = {
        'departments': Department.objects.all()
    }
    return render(request, 'deptlist.html', context)

@login_required
def delete_department(request, pk):
    dept = Department.objects.filter(pk=pk)
    if request.method == 'POST':
        dept.delete()
        return redirect('editdepartment')

#################################################################################

@login_required
def addBatches(request):
    form = BatchForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('addBatches')
    context = {
        'form': form
    }
    return render(request, 'addBatches.html', context)

@login_required
def batch_list(request):
    context = {
        'batches': Batch.objects.all()
    }
    return render(request, 'batchlist.html', context)

@login_required
def delete_batch(request, pk):
    batch = Batch.objects.filter(pk=pk)
    if request.method == 'POST':
        batch.delete()
        return redirect('editbatch')
    context = {
        'batch': batch
    }
    return render(request, 'delete_batch.html', context)

##################################################################################
@login_required
def addSections(request):
    form = SectionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('addSections')
    context = {
        'form': form
    }
    return render(request, 'addSections.html', context)

@login_required
def section_list(request):
    context = {
        'sections': Section.objects.all()
    }
    return render(request, 'seclist.html', context)

@login_required
def delete_section(request, pk):
    sec = Section.objects.filter(pk=pk)
    if request.method == 'POST':
        sec.delete()
        return redirect('editsection')

#################################################################################

@login_required
def generate(request):
    return render(request, 'generate.html', {})

#################################################################################



###############################################################################3


def index1(request):
    return render(request, 'my_login.html', {})

def about(request):
    return render(request, 'about.html', {})

def suggestion_thanks_view(request):
    return render(request, 'suggestion_thanks.html')

from django.shortcuts import render
from .forms import SuggestionForm


def suggestion_thanks(request):
    return render(request, 'suggestion_thanks.html')

def suggestion_view(request):
    if request.method == 'POST':
        form = SuggestionForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            suggestion = form.cleaned_data['suggestion']
            attachment = request.FILES.get('attachment')

            # Construct the mailto link
            subject = f'Suggestion from {name}'
            body = f"Name: {name}\nEmail: {email}\nSuggestion:\n{suggestion}"
            mailto_link = f"mailto:debadeba015@gmail.com?subject={subject}&body={body}"

            # Add the attachment part if the attachment is provided
            if attachment:
                mailto_link += f"&attachment={attachment.name}"

            return render(request, 'suggestion_redirect.html', {'mailto_link': mailto_link})
    else:
        form = SuggestionForm()
    
    return render(request, 'suggestion_form.html', {'form': form})

###################################################################################################

from django.shortcuts import render, redirect
from .models import PDF
from .forms import PDFUploadForm

def pdf_list(request):
    pdfs = PDF.objects.all()
    return render(request, 'pdf_list.html', {'pdfs': pdfs})

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lists')
    else:
        form = PDFUploadForm()
    return render(request, 'upload_pdf.html', {'form': form})

def view_pdf(request, pk):
    pdf = get_object_or_404(PDF, pk=pk)
    return render(request, 'view_pdf.html', {'pdf': pdf})

def lists(request):
    pdfs = PDF.objects.all()
    return render(request, 'list.html', {'pdfs': pdfs})

from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import PDF

@require_POST
def delete_pdf(request, pk):
    pdf = get_object_or_404(PDF, pk=pk)
    pdf.delete()
    return redirect('lists')

from django.shortcuts import render, redirect
from django.contrib import messages

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
       
        hardcoded_credentials = {
            'admin': 'password',  
        }
        
        if username in hardcoded_credentials:
            if hardcoded_credentials[username] == password:
               
                messages.success(request, "Login successful!")
                return redirect('index1')  
            else:
               
                messages.error(request, "Incorrect password.")
        else:
        
            messages.error(request, "Invalid username.")
    return render(request, 'adminlogin.html')

from django.shortcuts import get_object_or_404
from django.http import FileResponse
from .models import PDF

def download_pdf(request, pk):
    pdf = get_object_or_404(PDF, pk=pk)
    response = FileResponse(open(pdf.file.path, 'rb'), as_attachment=True)
    return response
