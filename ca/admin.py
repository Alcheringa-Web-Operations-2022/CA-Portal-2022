from django.contrib import admin
from .models import Idea, POC
from users.models import Profile
from ca.scores import IDEA_SCORE, POC_SCORE
from django.http import HttpResponse
import csv

class IdeaAdmin(admin.ModelAdmin):
	list_display = ('user', 'subject', 'idea', 'validate', 'ideascore' )
	list_filter = ("validate")
	search_fields = ['user']
	readonly_fields = ['ideascore']
	def save_model(self, request, obj, form, change):
		if 'validate' in form.changed_data:
			delta = IDEA_SCORE
			if obj.pk:
				old_value = Idea.objects.get(pk=obj.pk).validate
				if old_value == 1:
					delta = -IDEA_SCORE
				elif (old_value == -1 and obj.validate == 0) or (old_value == 0 and obj.validate == -1):
					delta = 0
			
			elif obj.validate != 1:
				delta = 0

			obj.ideascore+=delta
			obj.user.profile.score+=delta
		super().save_model(request, obj, form, change)
		obj.user.profile.save()

	def delete_model(self,request,obj):
		if obj.ideascore == IDEA_SCORE:
			obj.user.profile.score-=IDEA_SCORE

		super().delete_model(request,obj)
		obj.user.profile.save()


class POCAdmin(admin.ModelAdmin):
	list_display = ('user', 'name', 'design', 'college', 'contact', 'validate','POCscore')
	list_filter = ( "approval",)
	readonly_fields = ['POCscore',]
	# actions = ["approve_poc", "disapprove_poc",]

	def approve_poc(self, request, queryset):
		for poc in queryset:
			poc.validate=True
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
		if 'validate' in form.changed_data:
			delta = POC_SCORE
			if obj.pk:
				old_value = POC.objects.get(pk=obj.pk).validate
				if old_value == 1:
					delta = -POC_SCORE
				elif (old_value == -1 and obj.validate == 0) or (old_value == 0 and obj.validate == -1):
					delta = 0
				
			elif obj.validate != 1:
				delta = 0

			obj.POCscore+=delta
			obj.user.profile.score+=delta
			

		super().save_model(request, obj, form, change)
		obj.user.profile.save()

	def delete_model(self,request,obj):
		if obj.POCscore == POC_SCORE:
			obj.user.profile.score-=POC_SCORE


		super().delete_model(request,obj)
		obj.user.profile.save()

admin.site.register(Idea,IdeaAdmin)
admin.site.register(POC,POCAdmin)
