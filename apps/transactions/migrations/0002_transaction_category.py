from django.db import migrations, models

class Migration(migrations.Migration):
 
    dependencies = [
        ('transactions', '0001_initial'),
    ]
 
    operations = [
        migrations.AddField(
            model_name='transaction',
            name='category',
            field=models.CharField(
                choices=[
                    ('FOOD', 'Alimentação'),
                    ('TRANSPORT', 'Transporte'),
                    ('ENTERTAINMENT', 'Lazer'),
                    ('BILLS', 'Contas'),
                    ('SAVINGS', 'Poupança'),
                    ('HEALTH', 'Saúde'),
                    ('EDUCATION', 'Educação'),
                    ('OTHER', 'Outros'),
                ],
                default='OTHER',
                max_length=20,
                verbose_name='Categoria',
            ),
        ),
    ]