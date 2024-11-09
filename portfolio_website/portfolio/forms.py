# forms.py
from django import forms


from .models import Contact, Resume, PDFFile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit



class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)  # Make comments optional


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file', 'description']

class PDFFileForm(forms.ModelForm):
    class Meta:
        model = PDFFile
        fields = ['title', 'file']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('register', 'Register'))



class SharePostForm(forms.Form):
    name = forms.CharField(label="Your Name", max_length=100)
    email_to = forms.EmailField(label="Recipient's Email", max_length=254)
    comment = forms.CharField(widget=forms.Textarea, required=False, label="Add a personal message")

