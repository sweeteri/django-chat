# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import DirectMessage

class DirectMessageForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(queryset=User.objects.all(), required=True)

    class Meta:
        model = DirectMessage
        fields = ['recipient', 'content']