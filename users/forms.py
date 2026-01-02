from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from .models import UserProfile




class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username")
    first_name = forms.CharField(max_length=150, label="First Name")
    last_name = forms.CharField(max_length=150, label="Last Name")
    email = forms.EmailField(label="Email")
    phone_number = forms.CharField(max_length=20, required=False, label="Phone Number")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        
        UserProfile.objects.create(user=user)
        return user

    

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'dob', 'gender', 'level')
