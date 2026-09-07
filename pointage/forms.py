from django import forms

from .models import Employe, Horaire, Poste


class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = [
            'nom', 'prenom', 'email', 'telephone', 'poste', 'horaire',
            'date_embauche', 'actif',
        ]
        widgets = {
            'date_embauche': forms.DateInput(attrs={'type': 'date'}),
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
        fields = [
            'nom', 'type', 'heure_arrivee', 'heure_depart_midi',
            'heure_retour', 'heure_depart', 'tolerance_retard_minutes', 'actif',
        ]
        widgets = {
            'heure_arrivee': forms.TimeInput(attrs={'type': 'time'}),
            'heure_depart_midi': forms.TimeInput(attrs={'type': 'time'}),
            'heure_retour': forms.TimeInput(attrs={'type': 'time'}),
            'heure_depart': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('type') == Horaire.Type.CONTINU:
            cleaned_data['heure_depart_midi'] = None
            cleaned_data['heure_retour'] = None
        elif not cleaned_data.get('heure_depart_midi') or not cleaned_data.get('heure_retour'):
            raise forms.ValidationError(
                'Un horaire normal doit avoir une heure de départ midi et une heure de retour.'
            )
        return cleaned_data