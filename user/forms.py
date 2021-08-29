from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm

from .models import UserBase
from django import forms


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='Username',
        min_length=4,
        max_length=50,
        help_text='Required',
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your username"})
    )
    email = forms.EmailField(
        label='Email',
        help_text='Required',
        error_messages={'required': 'Enter a valid email'},
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your email"})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter your password"})
    )
    confirm = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm your password"})
    )

    class Meta:
        model = UserBase
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data["username"].lower()
        r = UserBase.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("That username has taken already.")
        return username

    def clean_confirm(self):
        cd = self.cleaned_data
        if cd["password"] != cd["confirm"]:
            raise forms.ValidationError("Passwords Must Match!")
        return cd["confirm"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError("That email has taken already. Try to log in")
        return email


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        label="Username",
        min_length=4,
        max_length=50,
        help_text="Required",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your username",
            "id": "login-username"
        })
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your password",
            "id": "login-password"
        })
    )


class EditForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email(Can not be changed)',
        help_text='Required',
        error_messages={'required': 'Enter a valid email'},
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Email",
            "readonly": "readonly",
            "id": "form-email"
        })
    )
    username = forms.CharField(
        label='Username(Can not be changed)',
        max_length=200,
        help_text='Required',
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Username",
            "readonly": "readonly",
            "id": "form-username"
        })
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "First Name",
            "id": "form-firstName",
        })
    )
    phone = forms.CharField(
        label="Phone",
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Phone Number",
            "id": "form-phone"
        })
    )
    post_code = forms.CharField(
        label="Post Code",
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Post Code",
            "id": "form-postCode"
        })
    )
    address1 = forms.CharField(
        label="Address Line 1",
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Address Line 1",
            "id": "form-address1"
        })
    )
    address2 = forms.CharField(
        label="Address Line 2",
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Address Line 2",
            "id": "form-address2"
        })
    )
    city = forms.CharField(
        label="City",
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "City",
            "id": "form-city"
        })
    )

    class Meta:
        model = UserBase
        fields = ("username", "email", "first_name", "phone", "post_code", "address1", "address2", "city")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].required = True
        self.fields["email"].required = True
        self.fields["first_name"].required = True


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email",
        })
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        u = UserBase.objects.get(email=email)
        if not u:
            raise forms.ValidationError("Email not found. Please try again")
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "New password",
        })
    )
    new_password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm password",
        })
    )

