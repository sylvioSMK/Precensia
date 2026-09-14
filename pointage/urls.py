from django.urls import path

from . import views

app_name = 'pointage'

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('admin/connexion/', views.ConnexionAdminView.as_view(), name='connexion'),
    path('admin/deconnexion/', views.deconnexion, name='deconnexion'),
    path('admin/dashboard/', views.dashboard, name='dashboard'),
    path('admin/employes/', views.employes, name='employes'),
    path('admin/employes/nouveau/', views.nouvel_employe, name='employe_nouveau'),
    path('admin/employes/<int:employe_id>/modifier/', views.modifier_employe, name='employe_modifier'),
    path('admin/postes/', views.postes, name='postes'),
    path('admin/postes/nouveau/', views.nouveau_poste, name='poste_nouveau'),
    path('admin/postes/<int:poste_id>/modifier/', views.modifier_poste, name='poste_modifier'),
    path('admin/horaires/', views.horaires, name='horaires'),
    path('admin/horaires/nouveau/', views.nouvel_horaire, name='horaire_nouveau'),
    path('admin/horaires/<int:horaire_id>/modifier/', views.modifier_horaire, name='horaire_modifier'),
    path('admin/presences/', views.presences, name='presences'),
    path('pointage/', views.pointage, name='pointage'),
    path('pointage/<int:employe_id>/<str:moment>/', views.enregistrer_pointage, name='enregistrer_pointage'),
    path('pointage/<int:employe_id>/', views.confirmation_pointage, name='confirmation_pointage'),
]