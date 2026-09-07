from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Employe, Horaire, Poste, Presence, Utilisateur


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
	list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
	fieldsets = UserAdmin.fieldsets + (('Rôle', {'fields': ('role',)}),)
	add_fieldsets = UserAdmin.add_fieldsets + (('Rôle', {'fields': ('role',)}),)


@admin.register(Poste)
class PosteAdmin(admin.ModelAdmin):
	list_display = ('nom', 'actif', 'date_creation')
	list_filter = ('actif',)
	search_fields = ('nom', 'description')


@admin.register(Horaire)
class HoraireAdmin(admin.ModelAdmin):
	list_display = ('nom', 'type', 'heure_arrivee', 'heure_depart', 'actif')
	list_filter = ('type', 'actif')
	search_fields = ('nom',)


@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
	list_display = ('nom', 'prenom', 'poste', 'horaire', 'actif')
	list_filter = ('actif', 'poste', 'horaire')
	search_fields = ('nom', 'prenom', 'email')


@admin.register(Presence)
class PresenceAdmin(admin.ModelAdmin):
	list_display = ('employe', 'date', 'statut', 'heure_arrivee', 'heure_depart')
	list_filter = ('statut', 'date')
	search_fields = ('employe__nom', 'employe__prenom')
