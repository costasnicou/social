from django import forms
from .models import *

class PostForm(forms.Form):
    content = forms.CharField(   
        label="Share your thoughts",
        required=True,
        widget=forms.Textarea(attrs={'class':'form-style form-control', 'placeholder':"What is in your mind?" })
    )

class EditPostForm(forms.Form):
    content = forms.CharField(   
        required=True,
        widget=forms.Textarea(attrs={'class':'form-style form-control' })
    )