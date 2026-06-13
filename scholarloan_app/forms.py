from django import forms

class ScholarshipSearchForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    age = forms.IntegerField(required=True)
    gpa = forms.FloatField(required=True, help_text="Enter your GPA (e.g., 3.5)")
    annual_income = forms.DecimalField(max_digits=10, decimal_places=2, required=True, help_text="Enter family annual income")
    course = forms.CharField(max_length=100, required=True, help_text="Enter your course (e.g., Computer Science)")

