from django.contrib.auth.models import AbstractUser
from django.db import models


class Utilisateur(AbstractUser):
	class Role(models.TextChoices):
		ADMIN = 'ADMIN', 'Administrateur'

	role = models.CharField(max_length=20, choices=Role.choices, default=Role.ADMIN)


class Poste(models.Model):
	nom = models.CharField(max_length=150)
	description = models.TextField(blank=True)
	actif = models.BooleanField(default=True)
	date_creation = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['nom']

	def __str__(self):
		return self.nom


class Horaire(models.Model):
	class Type(models.TextChoices):
		NORMAL = 'NORMAL', 'Normal'
		CONTINU = 'CONTINU', 'Continu'

	nom = models.CharField(max_length=150)
	type = models.CharField(max_length=10, choices=Type.choices, default=Type.NORMAL)
	heure_arrivee = models.TimeField()
	heure_depart_midi = models.TimeField(null=True, blank=True)
	heure_retour = models.TimeField(null=True, blank=True)
	heure_depart = models.TimeField()
	tolerance_retard_minutes = models.PositiveIntegerField(default=0)
	actif = models.BooleanField(default=True)

	class Meta:
		ordering = ['nom']

	def __str__(self):
		return self.nom


class Employe(models.Model):
	nom = models.CharField(max_length=150)
	prenom = models.CharField(max_length=150)
	email = models.EmailField(blank=True)
	telephone = models.CharField(max_length=30, blank=True)
	poste = models.ForeignKey(Poste, on_delete=models.PROTECT, related_name='employes')
	horaire = models.ForeignKey(Horaire, on_delete=models.PROTECT, related_name='employes')
	date_embauche = models.DateField()
	actif = models.BooleanField(default=True)
	date_creation = models.DateTimeField(auto_now_add=True)
	date_modification = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['nom', 'prenom']

	def __str__(self):
		return f'{self.prenom} {self.nom}'


class Presence(models.Model):
	class Statut(models.TextChoices):
		PRESENT = 'PRESENT', 'Présent'
		RETARD = 'RETARD', 'Retard'
		ABSENT = 'ABSENT', 'Absent'
		POINTAGE_INCOMPLET = 'POINTAGE_INCOMPLET', 'Pointage incomplet'

	employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='presences')
	date = models.DateField()
	heure_arrivee = models.TimeField(null=True, blank=True)
	heure_depart_midi = models.TimeField(null=True, blank=True)
	heure_retour = models.TimeField(null=True, blank=True)
	heure_depart = models.TimeField(null=True, blank=True)
	statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.POINTAGE_INCOMPLET)
	retard_minutes = models.PositiveIntegerField(null=True, blank=True)
	heures_travaillees = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

	class Meta:
		ordering = ['-date', 'employe__nom', 'employe__prenom']
		constraints = [
			models.UniqueConstraint(fields=['employe', 'date'], name='unique_presence_employe_date'),
		]

	def __str__(self):
		return f'{self.employe} - {self.date}'
