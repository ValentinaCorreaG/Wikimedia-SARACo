"""Forms for users app."""

from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile

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
        label="Usuario de Wikimedia",
        help_text="Debe coincidir exactamente con el nombre de usuario en Wikimedia/Wikipedia",
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Usuario de Wikimedia'
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
        wiki_username = self.cleaned_data["username"]
        user = User.objects.create_user(
            username=wiki_username,
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
        )
        user.set_unusable_password()
        user.is_staff = True
        user.is_superuser = role == "superuser"
        user.save()
        
        # Set the profile's professional_wiki_handle to match the username
        user.profile.professional_wiki_handle = wiki_username
        user.profile.save()
        
        return user


class ProfileEditForm(forms.ModelForm):
    """Form for editing user profile information."""
    
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
    email = forms.EmailField(
        required=False,
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'correo@ejemplo.com'
        })
    )

    class Meta:
        model = UserProfile
        fields = [
            'gender',
            'twitter',
            'facebook',
            'instagram',
            'linkedin',
            'wikidata_item',
            'orcid',
        ]
        labels = {
            'gender': 'Género',
            'twitter': 'Twitter',
            'facebook': 'Facebook',
            'instagram': 'Instagram',
            'linkedin': 'LinkedIn',
            'wikidata_item': 'Wikidata',
            'orcid': 'ORCID',
        }
        widgets = {
            'gender': forms.Select(attrs={'class': SELECT_CLASS}),
            'twitter': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': '@usuario'
            }),
            'facebook': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'usuario.facebook'
            }),
            'instagram': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': '@usuario'
            }),
            'linkedin': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'usuario-linkedin'
            }),
            'wikidata_item': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Q12345'
            }),
            'orcid': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': '0000-0000-0000-0000'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
        self.user = user

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
        if commit:
            profile.save()
        return profile
