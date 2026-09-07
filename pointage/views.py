from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render

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
	context = {
		'nombre_employes': Employe.objects.filter(actif=True).count(),
		'nombre_postes': Poste.objects.filter(actif=True).count(),
		'nombre_horaires': Horaire.objects.filter(actif=True).count(),
		'nombre_presences': Presence.objects.count(),
	}
	return render(request, 'pointage/dashboard.html', context)


@admin_required
def employes(request):
	return render(request, 'pointage/employes.html', {'employes': Employe.objects.select_related('poste', 'horaire')})


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
def page_simple(request, titre, **kwargs):
	return render(request, 'pointage/page_simple.html', {'titre': titre})


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
	return render(request, 'pointage/pointage.html', {'employes': Employe.objects.filter(actif=True)})


def confirmation_pointage(request, employe_id):
	employe = get_object_or_404(Employe, pk=employe_id, actif=True)
	return render(request, 'pointage/confirmation_pointage.html', {'employe': employe})
