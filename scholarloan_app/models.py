from django.db import models

class Scholarship(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    eligibility_criteria = models.TextField()
    gpa_requirement = models.FloatField(null=True, blank=True)
    income_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    age_limit = models.IntegerField(null=True, blank=True)
    available_for_courses = models.CharField(max_length=255, help_text="Comma-separated list of courses")
    deadline = models.DateField()

    def __str__(self):
        return self.name
    


