from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from course.models import Course
from enrollment.forms import CreateEnrollForm
from enrollment.models import Enroll


def index(request):
    enrolls = Enroll.objects.all()
    return render(request, 'enrollment/index.html', {'enrolls': enrolls})


def create(request):
    form = CreateEnrollForm()
    return render(request, 'enrollment/create.html', {'form': form})

@csrf_exempt
@require_POST
def get_course_total_amount(request):
    course_id = request.POST.get('course_id')
    if not course_id:
        return HttpResponseBadRequest('Missing course ID.')

    try:
        course = Course.objects.get(id=course_id)
        return JsonResponse({'data': float(course.fee or 0)})  # ✅ FIXED LINE
    except Course.DoesNotExist:
        return JsonResponse({'data': 0})


def store(request):
    if request.method == 'POST':
        form = CreateEnrollForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student enrolled successfully')
            return redirect('enroll.index')
        else:
            return render(request, 'enrollment/create.html', {'form': form})
    return redirect('enroll.index')


def edit(request, eid):
    enroll = get_object_or_404(Enroll, id=eid)
    form = CreateEnrollForm(instance=enroll)
    return render(request, 'enrollment/edit.html', {'form': form, 'enroll': enroll})


def update(request, eid):
    enroll = get_object_or_404(Enroll, id=eid)
    if request.method == 'POST':
        form = CreateEnrollForm(request.POST, instance=enroll)
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
            enroll.delete()
            messages.success(request, 'Enrollment deleted successfully')
        except Enroll.DoesNotExist:
            messages.error(request, 'Enrolled info not found')
    else:
        messages.error(request, 'Invalid request')
    return redirect('enroll.index')
