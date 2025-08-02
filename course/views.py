from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from course import models
from course.forms import CreateCourseForm, CreateFeeForm
from school.models import UserProfile
import json

# ✅ Utility: Get school linked to logged-in user
def get_user_school(request):
    if request.user.is_superuser:
        return None
    try:
        return request.user.userprofile.school
    except UserProfile.DoesNotExist:
        return None

def index(request):
    courses = models.Course.objects.all()
    return render(request, 'course/index.html', {'courses': courses})

def create(request):
    course = CreateCourseForm()
    fee = CreateFeeForm()
    return render(request, 'course/create.html', {'course': course, 'fee': fee})

def store(request):
    if request.method == 'POST':
        course_valid = CreateCourseForm(request.POST)
        fee_valid = CreateFeeForm(request.POST)

        try:
            fees_json = request.POST.get('fee_data', '[]')
            fees = json.loads(fees_json)
        except json.JSONDecodeError:
            fees = []

        # ✅ Defensive check
        school = get_user_school(request)
        if not school and not request.user.is_superuser:
            messages.error(request, "Your account is not linked to a school.")
            return redirect('course.create')

        if course_valid.is_valid():
            if fees and isinstance(fees, list):
                with transaction.atomic():
                    course = course_valid.save(commit=False)
                    course.school = school  # ✅ Assign school
                    course.save()

                    for fee_item in fees:
                        desc = fee_item.get('fee_desc', '').strip()
                        amount = fee_item.get('amount', 0)
                        if desc and amount:
                            models.Fee.objects.create(course=course, fee_desc=desc, amount=amount)

                    messages.success(request, 'Course created successfully')
                    return redirect('course.index')
            else:
                messages.warning(request, 'Please add at least one fee before submitting.')
                return redirect('course.create')
        else:
            return render(request, 'course/create.html', {'course': course_valid, 'fee': fee_valid})

    return redirect('course.create')

def edit(request, cid):
    try:
        course = models.Course.objects.get(id=cid)
        fee = models.Fee.objects.filter(course=course)
        course_form = CreateCourseForm(instance=course)
        fee_form = CreateFeeForm(instance=fee.last())
        return render(request, 'course/edit.html', {'course': course_form, 'fee': fee_form, 'fees': fee})
    except models.Course.DoesNotExist:
        return redirect('course.index')

def update(request, cid):
    if request.method == 'POST':
        try:
            course = models.Course.objects.get(id=cid)
            fee = models.Fee.objects.filter(course=course)
            course_form = CreateCourseForm(request.POST, instance=course)
            fee_form = CreateFeeForm(request.POST, instance=fee.last())

            try:
                fees_json = request.POST.get('fee_data', '[]')
                fees = json.loads(fees_json)
            except json.JSONDecodeError:
                fees = []

            # ✅ Defensive check
            school = get_user_school(request)
            if not school and not request.user.is_superuser:
                messages.error(request, "Your account is not linked to a school.")
                return redirect('course.edit', cid=cid)

            if course_form.is_valid():
                if fees and isinstance(fees, list):
                    with transaction.atomic():
                        fee.delete()
                        course = course_form.save(commit=False)
                        course.school = school  # ✅ Assign school
                        course.save()

                        for fee_item in fees:
                            desc = fee_item.get('fee_desc', '').strip()
                            amount = fee_item.get('amount', 0)
                            if desc and amount:
                                models.Fee.objects.create(course=course, fee_desc=desc, amount=amount)

                        messages.success(request, 'Course updated successfully')
                        return redirect('course.index')
                else:
                    messages.warning(request, 'Please add at least one fee before submitting.')
                    return redirect('course.edit', cid=cid)
            else:
                return render(request, 'course/edit.html', {'course': course_form, 'fee': fee_form, 'fees': fee})

        except models.Course.DoesNotExist:
            return redirect('course.index')

    return redirect('course.index')

def delete(request, cid):
    try:
        course = models.Course.objects.get(id=cid)
        course.delete()
        messages.success(request, 'Course deleted successfully')
        return redirect('course.index')
    except models.Course.DoesNotExist:
        return redirect('course.index')
