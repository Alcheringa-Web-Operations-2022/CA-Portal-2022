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
    return render(request, 'CA/register.html',{'form':form})





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
    return render(request,'CA/home.html', contextTasks)
    

@login_required
def ideas(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request,'CA/ideas.html',context)

@login_required
def poc(request):
    contextPOC = {
        'pocs': POC.objects.all()
    }
    return render(request,'CA/poc.html',contextPOC)

@login_required
def save_POC_from_csv(file_path):
    # do try catch accordingly
    # open csv file, read lines
    with open(file_path, 'r') as fp:
        pocs = csv.reader(fp, delimiter=',')
        row = 0
        for poc in pocs:
            if row==0:
                headers = poc
                row = row + 1
            else:
                # create a dictionary of student details
                new_poc_details = {}
                for i in range(len(headers)):
                    new_poc_details[headers[i]] = poc[i]

                # for the foreign key field current_class in Student you should get the object first and reassign the value to the key
                new_poc_details['user'] = User.objects.get() # get the record according to value which is stored in db and csv file

                # create an instance of Student model
                new_poc = POC()
                new_poc.__dict__.update(new_poc_details)
                new_poc.save()
                row = row + 1
        fp.close()

@login_required
def uploadcsv(request):
    if request.method == 'GET':
        form = POCBulkUploadForm()
        return render(request, 'ca/poc-csv.html', {'form':form})

    try:
        form = POCBulkUploadForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return redirect('ca/poc-csv.html')
            # If file is too large
            if csv_file.multiple_chunks():
                messages.error(request, 'Uploaded file is too big (%.2f MB)' %(csv_file.size(1000*1000),))
                return redirect('ca/poc-csv.html')

            # save and upload file 
            form.save()

            # get the path of the file saved in the server
            file_path = os.path.join(BASE_DIR, form.csv_file.url)

            # a function to read the file contents and save the student details
            save_POC_from_csv(file_path)
            # do try catch if necessary

    except:
        logging.getLogger('error_logger').error('Unable to upload file. ' + repr())
        messages.error(request, 'Unable to upload file. ' + repr())
    return redirect('ca/poc-csv.html')
    
