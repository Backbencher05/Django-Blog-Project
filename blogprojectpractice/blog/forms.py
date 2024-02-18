from django import forms
from blog.models import Comments
from django.contrib.auth.models import User

class EmailSendForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    # message and subject we will prepare dynamically depend upon post 
    # _

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('name', 'email', 'body')


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']