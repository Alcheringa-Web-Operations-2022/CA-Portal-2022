from django.contrib.auth.forms import UserCreationForm
from .models import POCBulkUpload

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class POCBulkUploadForm(forms.ModelForm):
  class Meta:
    model = POCBulkUpload
    fields = ("csv_file",)


