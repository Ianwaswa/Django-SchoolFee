from django import forms
from course.models import Course
from enrollment.models import Enroll
from student.models import Student


class CreateEnrollForm(forms.ModelForm):
    student_id = forms.ModelChoiceField(
        queryset=Student.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Student'
    )

    course_id = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Grade/Class'
    )

    total_fee = forms.FloatField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        label='Total Fee'
    )

    class Meta:
        model = Enroll
        fields = ['student_id', 'course_id', 'total_fee']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CreateEnrollForm, self).__init__(*args, **kwargs)

        if self.request:
            user = self.request.user
            if user.is_superuser:
                self.fields['student_id'].queryset = Student.objects.all()
                self.fields['course_id'].queryset = Course.objects.all()
            else:
                school = user.userprofile.school
                self.fields['student_id'].queryset = Student.objects.filter(school=school)
                self.fields['course_id'].queryset = Course.objects.filter(school=school)
