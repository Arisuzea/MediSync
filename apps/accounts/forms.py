from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from .models import BLOOD_TYPES, Patient

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"autofocus": True, "autocomplete": "username"}),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    error_messages = {
        **AuthenticationForm.error_messages,
        "invalid_login": "Incorrect username or password. Check both and try again.",
    }


class ProfileForm(forms.ModelForm):
    """Personal + health details. Name and email live on User, the rest on Patient."""

    full_name = forms.CharField(label="Full name", max_length=300)
    email = forms.EmailField(label="Email", required=False)

    class Meta:
        model = Patient
        fields = [
            "student_id", "course", "year_level", "phone",
            "blood_type", "allergies", "notes",
        ]
        labels = {
            "student_id": "Student ID",
            "year_level": "Year level",
            "phone": "Mobile",
            "blood_type": "Blood type",
            "allergies": "Allergies",
        }
        widgets = {"notes": forms.Textarea(attrs={"style": "min-height:96px"})}

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["full_name"].initial = user.get_full_name()
        self.fields["email"].initial = user.email
        # Show the form fields in the prototype's order.
        order = ["full_name", "student_id", "course", "year_level", "email", "phone",
                 "blood_type", "allergies", "notes"]
        self.order_fields(order)

    def clean_blood_type(self):
        value = self.cleaned_data["blood_type"].strip().upper()
        if value and value not in BLOOD_TYPES:
            raise forms.ValidationError(f"Use one of: {', '.join(BLOOD_TYPES)}.")
        return value

    def clean_student_id(self):
        return self.cleaned_data["student_id"] or None

    def save(self, commit=True):
        profile = super().save(commit=False)
        first, _, last = self.cleaned_data["full_name"].strip().rpartition(" ")
        if not first:  # a single word: treat it as the first name
            first, last = last, ""
        self.user.first_name = first[:150]
        self.user.last_name = last[:150]
        self.user.email = self.cleaned_data["email"]
        if commit:
            self.user.save(update_fields=["first_name", "last_name", "email"])
            profile.save()
        return profile


class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["emergency_name", "emergency_relationship", "emergency_phone"]
        labels = {
            "emergency_name": "Contact name",
            "emergency_relationship": "Relationship",
            "emergency_phone": "Mobile",
        }
