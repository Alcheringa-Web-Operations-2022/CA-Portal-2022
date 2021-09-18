from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from django import forms
from .models import Profile
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField
User = get_user_model()


class UserRegisterForm(UserCreationForm):
    DEGREE = [
        ('MBA', 'MBA'),
        ('BBA(Graduation)', 'BBA(Graduation)'),
        ('MTech/ME', 'MTech/ME'),
        ('Integrated/Dual Degree', 'Integrated/Dual Degree'),
        ('B.Tech/B.E', 'B.Tech/B.E'),
        ('M.A', 'M.A'),
        ('M.Sc.', 'M.Sc.'),
        ('M.Com.', 'M.Com.'),
        ('B.A.', 'B.A.'),
        ('B.Sc.', 'B.Sc.'),
        ('B.Com.', 'B.Com.'),
        ('Others', 'Others')
    ]
    DEPARTMENT = [
        ("Computer Science and Engineering", "Computer Science and Engineering"),
        ("Biosciences and Bioengineering", "Biosciences and Bioengineering"),
        ("Chemical Engineering", "Chemical Engineering"),
        ("Civil Engineering", "Civil Engineering"),
        ("Chemistry", "Chemistry"),
        ("Design", "Design"),
        ("Electronics and Electrical Engineering", "Electronics and Electrical Engineering"),
        ("Mechanical Engineering", "Mechanical Engineering"),
        ("Electronics and Communications Engineering", "Electronics and Communications Engineering"),
        ("Mathematics and Computing", "Mathematics and Computing"),
        ("Engineering Physics", "Engineering Physics"),
        ("Humanities and Social Sciences", "Humanities and Social Sciences")
    ]
    COURSE_DURATION = [
        ('1 year', '1 year'),
        ('2 year', '2 year'),
        ('3 year', '3 year'),
        ('4 year', '4 year'),
        ('5 year', '5 year'),
        ('6 year', '6 year'),
    ]
    GRADUATION_YEAR = [
        ('2020', '2020'),
        ('2021', '2022'),
        ('2022', '2022'),
        ('2023', '2023'),
        ('2024', '2024'),
        ('2025', '2025'),
        ('2026', '2026'),
        ('2027', '2027'),
    ]
    email = forms.EmailField(label="Email")
    firstname = forms.CharField(label="Full Name")
    phone = PhoneNumberField(widget=forms.TextInput(), label= "Phone number (e.g. +12125552368)", required=False)
    college = forms.CharField(label="College name")
    degree = forms.CharField(label="Course", widget=forms.Select(choices=DEGREE))
    department = forms.CharField(label="Course Specialization",  widget=forms.Select(choices=DEPARTMENT))
    course_duration = forms.CharField(label="Course Duration", widget=forms.Select(choices=COURSE_DURATION))
    graduation_year = forms.CharField(label="Year of Graduation", widget=forms.Select(choices=GRADUATION_YEAR))

    class Meta:
        model = User
        fields = ['firstname', 'email', 'phone', 'college', 'degree', 'department', 'course_duration' , 'graduation_year', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    DEGREE = [
        ('MBA', 'MBA'),
        ('BBA(Graduation)', 'BBA(Graduation)'),
        ('MTech/ME', 'MTech/ME'),
        ('Integrated/Dual Degree', 'Integrated/Dual Degree'),
        ('B.Tech/B.E', 'B.Tech/B.E'),
        ('M.A', 'M.A'),
        ('M.Sc.', 'M.Sc.'),
        ('M.Com.', 'M.Com.'),
        ('B.A.', 'B.A.'),
        ('B.Sc.', 'B.Sc.'),
        ('B.Com.', 'B.Com.'),
        ('Others', 'Others')
    ]
    DEPARTMENT = [
        ("Computer Science and Engineering", "Computer Science and Engineering"),
        ("Biosciences and Bioengineering", "Biosciences and Bioengineering"),
        ("Chemical Engineering", "Chemical Engineering"),
        ("Civil Engineering", "Civil Engineering"),
        ("Chemistry", "Chemistry"),
        ("Design", "Design"),
        ("Electronics and Electrical Engineering", "Electronics and Electrical Engineering"),
        ("Mechanical Engineering", "Mechanical Engineering"),
        ("Electronics and Communications Engineering", "Electronics and Communications Engineering"),
        ("Mathematics and Computing", "Mathematics and Computing"),
        ("Engineering Physics", "Engineering Physics"),
        ("Humanities and Social Sciences", "Humanities and Social Sciences")
    ]
    COURSE_DURATION = [
        ('1 year', '1 year'),
        ('2 year', '2 year'),
        ('3 year', '3 year'),
        ('4 year', '4 year'),
        ('5 year', '5 year'),
        ('6 year', '6 year'),
    ]
    GRADUATION_YEAR = [
        ('2020', '2020'),
        ('2021', '2022'),
        ('2022', '2022'),
        ('2023', '2023'),
        ('2024', '2024'),
        ('2025', '2025'),
        ('2026', '2026'),
        ('2027', '2027'),
    ]
    firstname = forms.CharField(label="Full Name")
    phone = PhoneNumberField(widget=forms.TextInput(), label= "Phone number (e.g. +12125552368)", required=False)
    college = forms.CharField(label="College name")
    degree = forms.CharField(label="Course", widget=forms.Select(choices=DEGREE))
    department = forms.CharField(label="Course Specialization",  widget=forms.Select(choices=DEPARTMENT))
    course_duration = forms.CharField(label="Course Duration", widget=forms.Select(choices=COURSE_DURATION))
    graduation_year = forms.CharField(label="Year of Graduation", widget=forms.Select(choices=GRADUATION_YEAR))

    class Meta:
        model = User
        fields = ['firstname', 'phone', 'college', 'degree', 'department', 'course_duration' , 'graduation_year']
