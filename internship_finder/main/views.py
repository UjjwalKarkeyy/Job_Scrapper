from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Internships

class Main_view(ListView):

    model = Internships
    paginate_by = 4


