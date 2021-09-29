from django.contrib import admin
from .models import POC
from django.http import HttpResponse
import csv,io
from ca.scores import POC_SCORE


class POCAdmin(admin.ModelAdmin):
	list_display = ('user', 'name', 'design', 'college', 'contact')
        list_filter = ("approval",)
	readonly_fields = ['POCscore',]

	def approve_poc(self, request, queryset):
		for poc in queryset:
			poc.approval=True
			poc.save()
		
		self.message_user(request, "All the selected PoCs have been approved successfully.")
	approve_poc.short_description = 'Approve all the selected PoCs'

	def disapprove_poc(self, request, queryset):
		for poc in queryset:
			poc.approval=False
			poc.save()
		self.message_user(request, "All the selected PoCs have been disapproved successfully.")
	disapprove_poc.short_description = 'Disapprove all the selected PoCs'
 
def save_model(self, request, obj, form, change):
		if 'approval' in form.changed_data:
			delta = POC_SCORE
			if obj.pk:
				old_value = POC.objects.get(pk=obj.pk).approval
				if old_value == 1:
					delta = -POC_SCORE
				elif (old_value == -1 and obj.approval == 0) or (old_value == 0 and obj.approval == -1):
					delta = 0
				
			elif obj.approval != 1:
				delta = 0

			obj.POCscore+=delta
			obj.user.ca_details.score+=delta
			#TriWeekly score function
			# if  delta > 0 or obj.triweeklyPOC!=0:
			# 	obj.triweeklyPOC+=delta
			# 	obj.user.ca_details.triweekly+=delta

		super().save_model(request, obj, form, change)
		obj.user.ca_details.save()

	def delete_model(self,request,obj):
		if obj.POCscore == POC_SCORE:
			obj.user.ca_details.score-=POC_SCORE

		#TriWeekly function
		# if obj.triweeklyPOC == POC_SCORE:
		# 	obj.user.ca_details.triweekly-=POC_SCORE
		super().delete_model(request,obj)
		obj.user.ca_details.save()


