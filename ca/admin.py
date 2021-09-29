from django.contrib import admin
from .models import POC
from django.http import HttpResponse
import csv,io


class POCAdmin(admin.ModelAdmin):
	list_display = ('user', 'name', 'design', 'college', 'contact')

	def approve_poc(self, request, queryset):
		for venue in queryset:
			venue.approval=True
			venue.save()
		
		self.message_user(request, "All the selected PoCs have been approved successfully.")
	approve_poc.short_description = 'Approve all the selected PoCs'

	def disapprove_poc(self, request, queryset):
		for venue in queryset:
			venue.approval=False
			venue.save()
		self.message_user(request, "All the selected PoCs have been disapproved successfully.")
	disapprove_poc.short_description = 'Disapprove all the selected PoCs'


