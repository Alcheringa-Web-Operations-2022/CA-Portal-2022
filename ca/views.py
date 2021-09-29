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
