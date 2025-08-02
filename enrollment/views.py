from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from course.models import Course
from enrollment.forms import CreateEnrollForm
from enrollment.models import Enroll
from student.models import Student


def get_user_school(request):
    return request.user.userprofile.school


def is_admin(request):
    return request.user.is_superuser


def index(request):
    if is_admin(request):
        enrolls = Enroll.objects.all()
    else:
        enrolls = Enroll.objects.filter(school=get_user_school(request))
    return render(request, 'enrollment/index.html', {'enrolls': enrolls})


def create(request):
    form = CreateEnrollForm(request=request)
    return render(request, 'enrollment/create.html', {'form': form})


@require_GET
def get_course_total_amount(request):
    course_id = request.GET.get('course_id')
    if not course_id:
        return HttpResponseBadRequest('Missing course ID.')
    try:
        course = Course.objects.get(id=course_id)
        return JsonResponse({'data': float(course.total_amount or 0)})
    except Course.DoesNotExist:
        return JsonResponse({'data': 0})


def store(request):
    if request.method == 'POST':
        form = CreateEnrollForm(request.POST, request=request)
        if form.is_valid():
            enroll = form.save(commit=False)
            enroll.school = get_user_school(request)
            enroll.save()
            messages.success(request, 'Student enrolled successfully')
            return redirect('enroll.index')
        else:
            return render(request, 'enrollment/create.html', {'form': form})
    return redirect('enroll.index')


def edit(request, eid):
    enroll = get_object_or_404(Enroll, id=eid)
    if not is_admin(request) and enroll.school != get_user_school(request):
        return redirect('enroll.index')
    form = CreateEnrollForm(instance=enroll, request=request)
    return render(request, 'enrollment/edit.html', {'form': form, 'enroll': enroll})


def update(request, eid):
    enroll = get_object_or_404(Enroll, id=eid)
    if not is_admin(request) and enroll.school != get_user_school(request):
        return redirect('enroll.index')
    if request.method == 'POST':
        form = CreateEnrollForm(request.POST, instance=enroll, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Enrolled info updated successfully')
            return redirect('enroll.index')
        else:
            return render(request, 'enrollment/edit.html', {'form': form, 'enroll': enroll})
    return redirect('enroll.index')


def delete(request, eid):
    if request.method == 'POST':
        try:
            enroll = Enroll.objects.get(id=eid)
            if is_admin(request) or enroll.school == get_user_school(request):
                enroll.delete()
                messages.success(request, 'Enrollment deleted successfully')
            else:
                messages.error(request, 'Permission denied.')
        except Enroll.DoesNotExist:
            messages.error(request, 'Enrolled info not found')
    else:
        messages.error(request, 'Invalid request')
    return redirect('enroll.index')
