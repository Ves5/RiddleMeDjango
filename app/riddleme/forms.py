from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', "aria-describedby":"passwordHelp"}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))