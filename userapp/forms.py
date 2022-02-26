import email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Profile, Skill
from django import forms 

User = get_user_model()

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=200, required=True)
    last_name = forms.CharField(max_length=200, required=True)
    username = forms.CharField(max_length=200, required=True)
    email1 = forms.EmailField(label="Email Address", required=True)
    email2 = forms.EmailField(label="Confirm Email Address", required=True)
    password1 = forms.CharField(widget=forms.PasswordInput,label='Password', required=True)
    password2 = forms.CharField(widget=forms.PasswordInput,label='Confirm Password', required=True )

    # fields = (first_name, last_name, username, email1, email2, password1, password2)
    # for field_ in fields:
    #     field_.widget.attrs.update({'class': 'input'})
    first_name.widget.attrs.update({'class':'input'})
    last_name.widget.attrs.update({'class':'input'})
    username.widget.attrs.update({'class':'input'})
    email1.widget.attrs.update({'class':'input'})
    email2.widget.attrs.update({'class':'input'})
    password1.widget.attrs.update({'class':'input'})
    password2.widget.attrs.update({'class':'input'})

    def clean_email2(self):
        email = self.cleaned_data.get("email1")
        confirm_email = self.cleaned_data.get("email2")

        if email.lower() != confirm_email.lower():
            raise ValidationError("Email did not match")
        
        return confirm_email

    def clean_password2(self):
        password = self.cleaned_data.get("password1")
        confirm_password = self.cleaned_data.get("password2")

        if password.lower() != confirm_password.lower():
            raise ValidationError("Password did not match")
        
        return confirm_password

    def clean_username(self):
        username = self.cleaned_data.get("username")
        q = User.objects.filter(username__iexact=username)
        if q.exists():
            raise ValidationError("This Username is already taken")
        return username

 

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "location short_intro bio profile_pic social_github\
            social_twitter social_linkedin social_youtube social_website".split()
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(SkillForm,self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})