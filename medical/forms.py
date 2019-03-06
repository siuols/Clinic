from django import forms
from .models import (
    Course,
    Department,
    Stock,
    Patient,
    History
    )
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils.translation import ugettext, ugettext_lazy as _

User = get_user_model()

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = [
			'number',                   
			'description',             
			'quantity',    
        ]

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = [
            'code',
            'description'
        ]

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'dept_code',
            'code',
            'description'
        ]

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'id_number',
            'last_name',
            'first_name',
            'middle_name',
            'course',
            'status'
        ]

class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = [
            'id_number',
            'item_code',
            'quantity',
            'complaints',
            'medication',
        ]

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', min_length=8, widget=forms.PasswordInput, validators=[RegexValidator('^[-a-zA-Z0-9_]+$', message="Password should be a combination of Alphabets and Numbers")])
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
                'username',
                'email'
            )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("Cannot use this email. It's already register")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        if qs.exists():
            raise forms.ValidationError("Username is already register")
        return username

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        #Save the provided password in hashed format
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True

        if commit:
            user.save()
        return user