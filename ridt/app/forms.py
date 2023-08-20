from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from app.models import Comment

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']



class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class':'md-textarea form-control',
        'placeholder':'Comment here...',
        'rows':'2'
    }))

    class Meta:
        model = Comment
        fields = ['content']
