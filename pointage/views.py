import calendar
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.db.models import Case, IntegerField, When
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import EmployeForm, HoraireForm, PosteForm
from .models import Employe, Horaire, Poste, Presence


admin_required = user_passes_test(lambda user: user.is_authenticated and user.is_staff)


def accueil(request):
	return redirect('pointage:pointage')


class ConnexionAdminView(LoginView):
	template_name = 'pointage/connexion.html'
	next_page = '/admin/dashboard/'


@admin_required
def dashboard(request):
	today = timezone.localdate()
	month_names = [
		'', 'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
		'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre',
	]
	context = {
		'nombre_employes': Employe.objects.filter(actif=True).count(),
		'nombre_postes': Poste.objects.filter(actif=True).count(),
		'nombre_horaires': Horaire.objects.filter(actif=True).count(),
		'nombre_presences': Presence.objects.count(),
		'aujourd_hui': today,
		'mois_courant': month_names[today.month],
		'semaines_calendrier': calendar.monthcalendar(today.year, today.month),
	}
	return render(request, 'pointage/dashboard.html', context)


@admin_required
def employes(request):
	return render(request, 'pointage/employes.html', {'employes': Employe.objects.select_related('poste')})


@admin_required
def postes(request):
	return render(request, 'pointage/postes.html', {'postes': Poste.objects.all()})


@admin_required
def nouveau_poste(request):
	form = PosteForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		form.save()
		return redirect('pointage:postes')
	return render(request, 'pointage/reference_form.html', {'form': form, 'titre': 'Nouveau poste', 'retour': 'pointage:postes'})


@admin_required
def modifier_poste(request, poste_id):
	poste = get_object_or_404(Poste, pk=poste_id)
	form = PosteForm(request.POST or None, instance=poste)
	if request.method == 'POST' and form.is_valid():
		form.save()
		return redirect('pointage:postes')
	return render(request, 'pointage/reference_form.html', {'form': form, 'titre': 'Modifier le poste', 'retour': 'pointage:postes'})


@admin_required
def horaires(request):
	return render(request, 'pointage/horaires.html', {'horaires': Horaire.objects.all()})


@admin_required
def nouvel_horaire(request):
	form = HoraireForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		form.save()
		return redirect('pointage:horaires')
	return render(request, 'pointage/reference_form.html', {'form': form, 'titre': 'Nouvel horaire', 'retour': 'pointage:horaires'})


@admin_required
def modifier_horaire(request, horaire_id):
	horaire = get_object_or_404(Horaire, pk=horaire_id)
	form = HoraireForm(request.POST or None, instance=horaire)
	if request.method == 'POST' and form.is_valid():
		form.save()
		return redirect('pointage:horaires')
	return render(request, 'pointage/reference_form.html', {'form': form, 'titre': "Modifier l'horaire", 'retour': 'pointage:horaires'})


@admin_required
def page_simple(request, titre, **kwargs):
	return render(request, 'pointage/page_simple.html', {'titre': titre})


@admin_required
def presences(request):
	date_selectionnee = timezone.localdate()
	date_param = request.GET.get('date')
	if date_param:
		try:
			date_selectionnee = datetime.strptime(date_param, '%Y-%m-%d').date()
		except ValueError:
			pass
	presences_du_jour = Presence.objects.filter(
		date=date_selectionnee,
		heure_arrivee__isnull=False,
	).select_related('employe', 'employe__poste').order_by(
		Case(
			When(statut=Presence.Statut.PRESENT, then=0),
			When(statut=Presence.Statut.RETARD, then=1),
			default=2,
			output_field=IntegerField(),
		),
		'heure_arrivee', 'employe__nom', 'employe__prenom'
	)
	return render(request, 'pointage/presences.html', {
		'presences': presences_du_jour,
		'date_selectionnee': date_selectionnee,
		'jour_precedent': date_selectionnee - timedelta(days=1),
		'jour_suivant': date_selectionnee + timedelta(days=1),
	})


@admin_required
def nouvel_employe(request):
	form = EmployeForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		form.save()
		return redirect('pointage:employes')
	return render(request, 'pointage/employe_form.html', {'form': form, 'titre': 'Nouvel employé'})


@admin_required
def modifier_employe(request, employe_id):
	employe = get_object_or_404(Employe, pk=employe_id)
	form = EmployeForm(request.POST or None, instance=employe)
	if request.method == 'POST' and form.is_valid():
		form.save()
		return redirect('pointage:employes')
	return render(request, 'pointage/employe_form.html', {'form': form, 'titre': 'Modifier un employé', 'employe': employe})


def pointage(request):
	today = timezone.localdate()
	presences = {
		presence.employe_id: presence
		for presence in Presence.objects.filter(date=today)
	}
	employes = list(Employe.objects.filter(actif=True).select_related('poste'))
	for employe in employes:
		employe.presence_du_jour = presences.get(employe.id)
	return render(request, 'pointage/pointage.html', {
		'employes': employes,
		'date_du_jour': today,
	})


def enregistrer_pointage(request, employe_id, moment):
	if request.method != 'POST':
		return redirect('pointage:pointage')
	employe = get_object_or_404(Employe, pk=employe_id, actif=True)
	champs_autorises = {
		'arrivee': 'heure_arrivee',
		'depart_midi': 'heure_depart_midi',
		'retour': 'heure_retour',
		'depart': 'heure_depart',
	}
	champ = champs_autorises.get(moment)
	if not champ or (moment in {'depart_midi', 'retour'} and employe.type_journee != Employe.TypeJournee.CONTINU):
		return redirect('pointage:pointage')
	maintenant = timezone.localtime()
	presence, _ = Presence.objects.get_or_create(employe=employe, date=timezone.localdate())
	if getattr(presence, champ) is None:
		setattr(presence, champ, maintenant.time().replace(microsecond=0))
		if champ == 'heure_arrivee':
			horaire = Horaire.objects.filter(actif=True).order_by('id').first()
			if horaire and maintenant.time() > horaire.heure_limite_retard:
				presence.statut = Presence.Statut.RETARD
			else:
				presence.statut = Presence.Statut.PRESENT
		presence.save()
	return redirect('pointage:pointage')


def confirmation_pointage(request, employe_id):
	employe = get_object_or_404(Employe, pk=employe_id, actif=True)
	return render(request, 'pointage/confirmation_pointage.html', {'employe': employe})
