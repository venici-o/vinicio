from django.db import migrations, models
import django.db.models.deletion


DEFAULT_CATEGORIES = [
    'Alimentação',
    'Transporte',
    'Poupança',
    'Saúde',
    'Educação',
    'Lazer',
    'Salário',
    'Outros',
]


def populate_default_categories(apps, schema_editor):
    Category = apps.get_model('transactions', 'Category')
    for name in DEFAULT_CATEGORIES:
        Category.objects.get_or_create(user=None, name=name)


def remove_default_categories(apps, schema_editor):
    Category = apps.get_model('transactions', 'Category')
    Category.objects.filter(user=None).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_transaction_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('user', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    to='auth.user',
                    verbose_name='Usuário',
                )),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.RunPython(populate_default_categories, remove_default_categories),
        migrations.RemoveField(
            model_name='transaction',
            name='category',
        ),
        migrations.AddField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='transactions.category',
                verbose_name='Categoria',
            ),
        ),
    ]
