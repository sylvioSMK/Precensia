from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pointage', '0002_rename_heure_arrivee_horaire_heure_limite_retard_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employe',
            name='date_embauche',
        ),
        migrations.AlterField(
            model_name='employe',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]