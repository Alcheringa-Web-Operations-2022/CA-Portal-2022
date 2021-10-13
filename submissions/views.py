from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView

from dashboard.models import Notifications
from .models import POC, Idea, Media, POCBulk, Submission
from django.http import JsonResponse
import json
from .forms import POCBulkForm, POCForm, IdeaForm, MediaForm
from django.contrib import messages
from django import forms
from django.conf import settings

from django.db.models import Q


class IdeaCreateView(CreateView):
    model = Idea
    form_class = IdeaForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(
            self.request, f'Your idea has been submitted! Verification - Pending')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(IdeaCreateView, self).get_context_data(**kwargs)
        notification_list = Notifications.objects.filter(
            Q(user=self.request.user) | Q(user=None)).order_by('-created_on')
        ctx['notification_list'] = notification_list
        ctx['heading'] = 'Submissions'
        return ctx


class POCCreateView(CreateView):
    model = POC
    form_class = POCForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(
            self.request, f'Your POC has been submitted! Verification - Pending')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(POCCreateView, self).get_context_data(**kwargs)
        notification_list = Notifications.objects.filter(
            Q(user=self.request.user) | Q(user=None)).order_by('-created_on')
        ctx['notification_list'] = notification_list
        ctx['heading'] = 'Submissions'
        return ctx


class POCBulkCreateView(CreateView):
    model = POCBulk
    form_class = POCBulkForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(
            self.request, f'Your POCs has been submitted! Verification - Pending')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(POCBulkCreateView, self).get_context_data(**kwargs)
        notification_list = Notifications.objects.filter(
            Q(user=self.request.user) | Q(user=None)).order_by('-created_on')
        ctx['notification_list'] = notification_list
        ctx['heading'] = 'Submissions'
        return ctx


class MediaCreateView(CreateView):
    model = Media
    form_class = MediaForm

    def get_form(self):
        data = json.loads(self.request.body)
        return MediaForm({
            "shared_post": data.get("shared_post")
        })

    def form_invalid(self, form):
        response = super(MediaCreateView, self).form_invalid(form)
        print(form)
        print(self.request.POST)
        return JsonResponse({
            "success": False,
            "error": form.errors
        }, status=400)

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super(MediaCreateView, self).form_valid(form)
        data = {
            "success": True,
            'message': "Successfully submitted form data."
        }
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        ctx = super(MediaCreateView, self).get_context_data(**kwargs)
        notification_list = Notifications.objects.filter(
            Q(user=self.request.user) | Q(user=None)).order_by('-created_on')
        ctx['notification_list'] = notification_list
        ctx['heading'] = 'Submissions'
        return ctx


@login_required(login_url='dashboard_page')
def home(request):
    notification_list = Notifications.objects.filter(
        Q(user=request.user) | Q(user=None)).order_by('-created_on')
    return render(request, 'submissions/home.html', {'heading': 'Submissions', 'notification_list': notification_list})


@login_required(login_url='dashboard_page')
def tasks(request):
    notification_list = Notifications.objects.filter(
        Q(user=request.user) | Q(user=None)).order_by('-created_on')
    return render(request, 'submissions/tasks.html', {'heading': 'Tasks', 'notification_list': notification_list})


@login_required(login_url='dashboard_page')
def ideas(request):
    userNow = request.user
    notification_list = Notifications.objects.filter(
        Q(user=request.user) | Q(user=None)).order_by('-created_on')
    context = {
        'ideas': userNow.idea_submissions.all(), 'notification_list': notification_list
    }
    return render(request, 'submissions/ideas.html', context)


@login_required(login_url='dashboard_page')
def pocs(request):
    userNow = request.user
    notification_list = Notifications.objects.filter(
        Q(user=request.user) | Q(user=None)).order_by('-created_on')
    context = {
        'pocs': userNow.poc_submissions.all(), 'notification_list': notification_list
    }
    return render(request, 'submissions/pocs.html', context)
