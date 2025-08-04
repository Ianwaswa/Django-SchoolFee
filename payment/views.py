from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from course.models import Fee
from enrollment.models import Enroll
from payment.forms import CreatePaymentForm, DateSelectionForm
from payment.models import Payment, Action
from school.models import UserProfile

# ✅ Safe school getter
def get_user_school(request):
    if request.user.is_superuser:
        return None
    try:
        return request.user.userprofile.school
    except UserProfile.DoesNotExist:
        return None

def is_admin(request):
    return request.user.is_superuser

def index(request):
    if is_admin(request):
        payments = Payment.objects.all()
    else:
        school = get_user_school(request)
        if not school:
            messages.error(request, "Your account is not linked to a school.")
            return redirect('dashboard')  # Or any fallback
        payments = Payment.objects.filter(school=school)
    return render(request, 'payment/index.html', {'payments': payments})

def create(request):
    form = CreatePaymentForm(request=request)
    return render(request, 'payment/create.html', {'form': form})

def store(request):
    if request.method == 'POST':
        form = CreatePaymentForm(request.POST, request=request)
        if form.is_valid():
            with transaction.atomic():
                payment = form.save(commit=False)
                payment.created_by = request.user
                school = get_user_school(request)
                if not school and not is_admin(request):
                    messages.error(request, "Your account is not linked to a school.")
                    return redirect('payment.create')
                payment.school = school
                payment.save()
                Action.objects.create(sender=request.user, verb="created this payment", target=payment)
                messages.success(request, 'Payment created successfully')
            return redirect('payment.index')
        else:
            return render(request, 'payment/create.html', {'form': form})
    return redirect('payment.create')

@require_POST
def get_outstanding_balance(request):
    try:
        enroll_id = request.POST.get('enroll_id')
        enroll = Enroll.objects.get(id=enroll_id)
        if is_admin(request) or enroll.school == get_user_school(request):
            return JsonResponse({'data': float(enroll.balance)})
        else:
            return JsonResponse({'data': 0})
    except Enroll.DoesNotExist:
        return JsonResponse({'data': 0})

def edit(request, pid):
    try:
        payment = Payment.objects.get(id=pid)
        if not is_admin(request) and payment.school != get_user_school(request):
            return redirect('payment.index')
        form = CreatePaymentForm(instance=payment, request=request)
        return render(request, 'payment/edit.html', {'form': form})
    except Payment.DoesNotExist:
        messages.error(request, 'Payment does not exist')
        return redirect('payment.index')

def update(request, pid):
    if request.method == 'POST':
        try:
            payment = Payment.objects.get(id=pid)
            if not is_admin(request) and payment.school != get_user_school(request):
                return redirect('payment.index')
            form = CreatePaymentForm(request.POST, instance=payment, request=request)
            if form.is_valid():
                with transaction.atomic():
                    form.save()
                    Action.objects.create(sender=request.user, verb="updated this payment", target=form.instance)
                    messages.success(request, 'Payment updated successfully')
                return redirect('payment.index')
            else:
                return render(request, 'payment/edit.html', {'form': form})
        except Payment.DoesNotExist:
            messages.error(request, 'Payment does not exist')
    return redirect('payment.index')

def delete(request, pid):
    if request.method == 'POST':
        if not is_admin(request):
            messages.error(request, 'Only administrators can delete payments.')
            return redirect('payment.index')

        try:
            payment = Payment.objects.get(id=pid)
            with transaction.atomic():
                Action.objects.create(sender=request.user, verb="deleted this payment", target=payment)
                payment.delete()
                messages.success(request, 'Payment deleted successfully')
        except Payment.DoesNotExist:
            messages.error(request, 'Payment does not exist')

    return redirect('payment.index')

def invoice(request, pid):
    try:
        payment = Payment.objects.get(id=pid)
        if not is_admin(request) and payment.school != get_user_school(request):
            return redirect('payment.index')
        fees = Fee.objects.filter(course_id=payment.enroll_id.course_id)
        history = Payment.objects.filter(enroll_id=payment.enroll_id, id__lte=payment.id)
        return render(request, 'payment/invoice.html', {'pay_current': payment, 'pay_history': history, 'fees': fees})
    except Payment.DoesNotExist:
        messages.error(request, 'Payment does not exist')
        return redirect('payment.index')

def report(request):
    form = DateSelectionForm()
    month = request.GET.get('month')
    year = request.GET.get('year')

    if is_admin(request):
        queryset = Payment.objects.all()
    else:
        school = get_user_school(request)
        if not school:
            messages.error(request, "Your account is not linked to a school.")
            return redirect('dashboard')
        queryset = Payment.objects.filter(school=school)

    if month and year:
        queryset = queryset.filter(date_created__month=month, date_created__year=year)

    return render(request, 'payment/report.html', {'form': form, 'payments': queryset})
