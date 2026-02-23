"""Forms for users app."""

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

INPUT_CLASS = 'w-full px-4 py-2 border border-primary-200 rounded-lg focus:ring-2 focus:ring-primary-300 focus:border-transparent'
SELECT_CLASS = 'w-full px-4 py-2 border border-primary-200 rounded-lg focus:ring-2 focus:ring-primary-300 focus:border-transparent'


class UserCreationByRoleForm(forms.Form):
    """Create a Django user and assign a privileged role."""

    ROLE_CHOICES = (
        ("staff", "Staff"),
        ("superuser", "Superusuario"),
    )

    username = forms.CharField(
        max_length=150,
        label="Usuario",
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Nombre de usuario'
        })
    )
    email = forms.EmailField(
        required=False,
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'correo@ejemplo.com'
        })
    )
    first_name = forms.CharField(
        max_length=150,
        required=False,
        label="Nombre",
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Nombre'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        label="Apellido",
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Apellido'
        })
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label="Rol",
        widget=forms.Select(attrs={
            'class': SELECT_CLASS
        })
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya existe.")
        return username

    def save(self):
        role = self.cleaned_data["role"]
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
        )
        user.set_unusable_password()
        user.is_staff = True
        user.is_superuser = role == "superuser"
        user.save()
        return user
