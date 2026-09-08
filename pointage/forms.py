from django import forms

from .models import Employe, Horaire, Poste


class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = [
            'nom', 'prenom', 'email', 'telephone', 'poste', 'type_journee',
            'actif',
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Optionnel'}),
        }


class PosteForm(forms.ModelForm):
    class Meta:
        model = Poste
        fields = ['nom', 'description', 'actif']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class HoraireForm(forms.ModelForm):
    class Meta:
        model = Horaire
        fields = ['nom', 'heure_limite_retard', 'actif']
        widgets = {
            'heure_limite_retard': forms.TimeInput(attrs={'type': 'time'}),
        }
