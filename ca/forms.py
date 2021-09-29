class POCbulkForm(forms.ModelForm):
  class Meta:
    model = POCbulk
    fields = ("csv_file",)
