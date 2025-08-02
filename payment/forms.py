from datetime import datetime

from django import forms

from enrollment.models import Enroll
from payment.models import Payment


class CreatePaymentForm(forms.ModelForm):
    enroll_id = forms.ModelChoiceField(
        label='Enrollment',
        queryset=Enroll.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    balance = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        label='Balance',
        required=False
    )
    amount = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Amount'
    )
    remarks = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label='Remarks'
    )

    class Meta:
        model = Payment
        fields = ['enroll_id', 'balance', 'amount', 'remarks']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CreatePaymentForm, self).__init__(*args, **kwargs)

        if self.request:
            user = self.request.user
            if user.is_superuser:
                self.fields['enroll_id'].queryset = Enroll.objects.all()
            else:
                school = user.userprofile.school
                self.fields['enroll_id'].queryset = Enroll.objects.filter(school=school)


class DateSelectionForm(forms.Form):
    MONTH_CHOICES = (
        (1, "Jan"),
        (2, "Feb"),
        (3, "Mar"),
        (4, "Apr"),
        (5, "May"),
        (6, "Jun"),
        (7, "Jul"),
        (8, "Aug"),
        (9, "Sep"),
        (10, "Oct"),
        (11, "Nov"),
        (12, "Dec"),
    )

    month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        initial=datetime.now().month,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    YEAR_CHOICES = [(r, r) for r in range(2020, 2040)]
    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        initial=datetime.now().year,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
