from datetime import datetime

from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render

from enrollment.models import Enroll
from payment.models import Payment, Action
from student.models import Student


def get_user_school(request):
    # Return the user's school if available, else None
    try:
        return request.user.userprofile.school
    except AttributeError:
        return None


def index(request):
    school = get_user_school(request)

    if school:
        payments = Payment.objects.filter(school=school).order_by('-date_created')[:10]
        enroll_count = Enroll.objects.filter(school=school).count()
        student_count = Student.objects.filter(school=school).count()
    else:
        payments = Payment.objects.all().order_by('-date_created')[:10]
        enroll_count = Enroll.objects.all().count()
        student_count = Student.objects.all().count()

    earnings = {}
    for month in range(1, 13):
        qset = Payment.objects.filter(date_created__month=month)
        if school:
            qset = qset.filter(school=school)
        earnings[month] = qset.aggregate(Sum('amount'))['amount__sum'] or 0

    monthly = earnings.get(datetime.now().month, 0)
    annual = sum(earnings.values())

    return render(request, 'index.html', {
        'payment': payments,
        'earnings': earnings,
        'monthly': monthly,
        'annual': annual,
        'enroll': enroll_count,
        'students': student_count,
    })


def activity(request):
    school = get_user_school(request)

    if school:
        payment_activity = Action.objects.filter(school=school).order_by('-created')
    else:
        payment_activity = Action.objects.all().order_by('-created')

    return render(request, 'activity/index.html', {
        'payment_activity': payment_activity
    })
