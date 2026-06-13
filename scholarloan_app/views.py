from django.shortcuts import render
from .models import Scholarship
from .forms import ScholarshipSearchForm
import requests
def home(request):
    return render(request, 'home.html')




# Dashboard View
def dashboard(request):
    return render(request, 'dashboard.html')


# Chatbot Page
def chatbot(request):
    return render(request, 'chatbot.html')
def login_view(request):
    return render(request, 'login.html') 


import requests
from django.shortcuts import render

# Google Custom Search API credentials
API_KEY = "xxxxxxxxxxxxxxxx"
SEARCH_ENGINE_ID = "xxxxxxxxxxxxxx"

def find_scholarships(request):
    scholarships = []
    
    if request.method == "POST":
        name = request.POST.get("name")
        cgpa = request.POST.get("cgpa")
        category = request.POST.get("category")
        income = request.POST.get("income")
        education_level = request.POST.get("education_level")
        course = request.POST.get("course")  # New field for Course of Study
        country = request.POST.get("country")
        gender = request.POST.get("gender")
        # Construct search query
        query = f"{education_level} scholarships for {gender} {course} students in {country} for {category} category site:scholarships.com OR site:fastweb.com OR site:scholarships.gov.in OR site:buddy4study.com OR site:scholarship-positions.com"

        # API request URL

        # API request URL
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}"

        # Make API request
        response = requests.get(url)
        data = response.json()

        # Extract search results
        if "items" in data:
            scholarships = [
                {"title": item["title"], "link": item["link"], "snippet": item.get("snippet", "No description available")}
                for item in data["items"]
            ]
    
    return render(request, "find_scholarships.html", {"scholarships": scholarships})

