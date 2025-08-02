from django import forms
from student.models import Student
from course.models import Course

class CreateStudentForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    contact = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=200, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': '3'
    }))
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_course'}),
        label='Grade/Class'
    )

    class Meta:
        model = Student
        fields = ['name', 'email', 'contact', 'address', 'course']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateStudentForm, self).__init__(*args, **kwargs)

        if not self.user.is_superuser:
            school = self.user.userprofile.school
            self.fields['course'].queryset = Course.objects.filter(school=school)
