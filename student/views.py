# student/views.py
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from . import models, forms
from course.models import Course  # Import Course model to use in AJAX response


# View all students
def index(request):
    students = models.Student.objects.all()
    return render(request, 'student/index.html', {'students': students})


# Show form to create a new student
def create(request):
    form = forms.CreateStudentForm()
    return render(request, 'student/create.html', {'form': form})


# Store student to DB
def store(request):
    if request.method == 'POST':
        form = forms.CreateStudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student created successfully')
            return redirect('student.index')
        else:
            return render(request, 'student/create.html', {'form': form})
    return redirect('student.create')


# Get fee for a selected course (AJAX)
def get_course_fee(request):
    course_id = request.GET.get('course_id')
    if course_id:
        try:
            course = Course.objects.get(pk=course_id)
            return JsonResponse({'fee': course.total_amount})
        except Course.DoesNotExist:
            return JsonResponse({'fee': 0})
    return JsonResponse({'fee': 0})


# Edit existing student
def edit(request, sid):
    try:
        student = models.Student.objects.get(id=sid)
        form = forms.CreateStudentForm(instance=student)
        return render(request, 'student/edit.html', {'form': form})
    except models.Student.DoesNotExist:
        return redirect('student.index')


# Update student
def update(request, sid):
    if request.method == 'POST':
        try:
            student = models.Student.objects.get(id=sid)
            form = forms.CreateStudentForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, 'Student updated successfully')
                return redirect('student.index')
            else:
                return render(request, 'student/edit.html', {'form': form})
        except models.Student.DoesNotExist:
            return redirect('student.index')
    return redirect('student.index')


# Delete student
def delete(request, sid):
    if request.method == 'POST':
        try:
            student = models.Student.objects.get(id=sid)
            student.delete()
            messages.success(request, 'Student deleted successfully')
        except models.Student.DoesNotExist:
            pass
    return redirect('student.index')
