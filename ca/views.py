from django.shortcuts import render, redirect
import csv,io
from ca.models import POC,POC_form
from django.contrib import messages 
from django.contrib.auth.decorators import login_required,permission_required
from django.http import JsonResponse
from django.core.validators import RegexValidator, EmailValidator, URLValidator
from django.contrib.auth.models import User


@permission_required('admin_can_add_log_entry')

def poc(request):
    template="poc.html"

    prompt={
        'order : Order of CSV should be Name,Designation,College,Contact '
    }

    if request.method == "GET": 
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request,'this is not a CSV File')

    data_set = csv.file.read().decode('UTF-8')
    io_string = io.stringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string,delimiter=',',quotechar="|") :

        _, created = POC.objects.update_or_create(
            name=column[0],
            design=column[1],
            college=column[2],
            contact=column[3]
        )
        
        context = {}

        return render(request,template,context)
    
  
@login_required
def poc_form(request):
        if request.method == 'POST':
                
                data = {}
                if request.POST['poc_name'] == '':
                        data['poc_name'] = "Name Empty"
                
                if request.POST['poc_design'] == '':
                        data['poc_design'] = "Designation Empty"

                if request.POST['poc_college'] == '':
                        data['poc_college'] = "College Empty"

                if request.POST['poc_phone'] == '':
                                         data['poc_phone'] = "Phone Empty"
                else:
                        contact_number_validator = RegexValidator('^[0-9]{10}$')
                        try:
                                contact_number_validator(request.POST['poc_phone'])
                        except Exception as e:
                                data['poc_phone'] = "Phone REGEX"
                if data:
                        data['stat'] = "FAILURE"
                        return JsonResponse(data)
                else :
                        poc_name = request.POST['poc_name']
                        poc_design= request.POST['poc_design']
                        poc_college = request.POST['poc_college']
                        poc_phone = request.POST['poc_phone']

                        POC.objects.create(user=request.user,name=poc_name, design=poc_design,
                                clg=poc_college, contact=poc_phone)
                        data['stat'] = "Success"

                        return JsonResponse(data)
        else:
                
                poc_queries = POC.objects.filter(user=request.user)
                context = {
                        'more_active': True,
                        'poc_queries': poc_queries
                }
                return render(request, 'ca/poc.html', context)
