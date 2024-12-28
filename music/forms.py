from django import forms
from .models import UserBehavior

class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserBehavior
        fields = ['favorited', 'play_count'] 