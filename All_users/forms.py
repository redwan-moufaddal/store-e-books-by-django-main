from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, required=True, widget=forms.TextInput(attrs={'class': 'mb-0 form-control', 'id': 'email', 'placeholder': 'Enter Your Email Address Here..'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'mb-0 form-control', 'id': 'password1', 'placeholder': 'Enter your password'}), required=True)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'mb-0 form-control', 'id': 'password2', 'placeholder': 'Confirm your password'}), required=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_password2(self):
        # Ensure passwords match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2

    def save(self, commit=True):
        # Create a new user
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email
