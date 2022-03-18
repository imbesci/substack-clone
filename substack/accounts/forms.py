from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import SubstackUser
from django.forms.models import modelformset_factory, modelform_factory

class SubstackUserCreation(UserCreationForm):
    email = forms.EmailField(max_length=60, min_length = 6,
                            help_text = 'Please enter a valid email address (required).'
                            )

    class Meta:
        model = SubstackUser
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
        

class SubstackAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = SubstackUser
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login, please try again")


class SubstackUpdateForm(forms.ModelForm):
    
    class Meta:
        model = SubstackUser
        fields = ('email', 'username')
    
    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = SubstackUser.objects.exclude(pk=self.instance.pk).get(email=email)
            except SubstackUser.DoesNotExist:
                return email
            raise forms.ValidationError('The email "%s" is already in use.' % account.email)

    def clean_username(self):
        if self.is_valid():
            username  = self.cleaned_data['username']
            try:
                account = SubstackUser.objects.exclude(pk=self.instance.pk).get(email=username)
            except SubstackUser.DoesNotExist:
                return username
            raise forms.ValidationError('The username "%s" is already in use.' % account.username)

class SubstackAccountUpdate(forms.ModelForm):
    class Meta:
        model = SubstackUser
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',  
        )

SubstackAccountUpdateFormset = modelformset_factory(SubstackUser, fields = ('first_name', 'last_name', 'email', 'username' ))