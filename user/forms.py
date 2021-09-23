from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm

from .models import UserBase, Address
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
    mobile = forms.CharField(
        label="Phone Number",
        max_length=50,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Phone Number",
            "id": "form-phone"
        })
    )

    class Meta:
        model = UserBase
        fields = ("username", "email", "first_name", "mobile")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].required = True
        self.fields["email"].required = True
        self.fields["first_name"].required = True
        self.fields["mobile"].required = True


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


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "phone", "address_line", "address_line2", "postcode", "town_base"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["phone"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Phone Number"}
        )
        self.fields["address_line"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Address Line 1"}
        )
        self.fields["address_line2"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Address Line 2"}
        )
        self.fields["postcode"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Post Code"}
        )
        self.fields["town_base"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Town City"}
        )





