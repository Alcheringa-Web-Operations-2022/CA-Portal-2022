from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from CAPortal.settings import BASE_DIR
from .forms import UserRegisterForm,POCBulkUploadForm
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .models import Post, Tasks, POC
from django.contrib import messages
import csv,io,os,logging


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'ca/register.html',{'form':form})





class PostCreateView(CreateView):
    model=Post
    fields = ['subject', 'tell_us_your_idea']

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.warning(self.request, f'Your idea has been submitted! Verification - Pending')
        return super().form_valid(form)

class POCCreateView(CreateView):
    model=POC
    fields = ['name', 'design','college','contact']

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.warning(self.request, f'Your POC has been submitted! Verification - Pending')
        return super().form_valid(form)

@login_required
def home(request):
    contextTasks = {
        'tasks': Tasks.objects.all()
    }
    return render(request,'ca/home.html', contextTasks)
    

@login_required
def ideas(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request,'ca/ideas.html',context)

@login_required
def poc(request):
    contextPOC = {
        'pocs': POC.objects.all()
    }
    return render(request,'ca/poc.html',contextPOC)

# one parameter named request
def poccsv(request):
    # declaring template
    template = "poc-csv.html"
    data = POC.objects.all()
# prompt is a context variable that can have different values      depending on their context
    prompt = {
        'order': 'Order of the CSV should be name, designation,college, contact',
        'profiles': data    
              }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['file']
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line we are able to handle a data in a stream
io_string = io.StringIO(data_set)
next(io_string)
for column in csv.reader(io_string, delimiter=',', quotechar="|"):
    _, created = POC.objects.update_or_create(
        name=column[0],
        design=column[1],
        college=column[2],
        contact=column[3]
    )
context = {}
return render(request, template, context)
