import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bank_accounts", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="conta",
            name="usuario",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="conta",
            name="agency",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name="conta",
            name="nickname",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
