from django import forms
from django.contrib.auth.models import User

class ChangeUsernamePasswordForm(forms.ModelForm):
    username = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "New Username"})
    )
    password = forms.CharField(
        required=False, 
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "New Password (Optional)"})
    )

    class Meta:
        model = User
        fields = ["username", "password"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
