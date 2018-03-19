from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.forms import ModelForm


class SignUpForm(UserCreationForm):
    #first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2', )

class property_detail_form(ModelForm):
    def clean_document(self):
        apartment_image = self.cleaned_data['apartment_image']
        if hasattr(apartment_image, '_size'):
            if document.size > settings.MAX_UPLOAD_SIZE:
                error_msg = 'Bitte Dateigrösse unter %s halten. Aktuelle Dateigrösse ist %s'
                sizes = filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(apartment_image._size)
                raise forms.ValidationError(error_msg % sizes)
            
            return apartment_image
    #image = forms.ImageField()

    class Meta:
        model = common_detail
        fields = ('apartment_name','apartment_type','county','rent','location','phone','apartment_image','description')


