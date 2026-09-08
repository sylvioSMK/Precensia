from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pointage', '0003_remove_employe_date_embauche_and_require_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employe',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]