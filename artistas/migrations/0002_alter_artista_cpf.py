# Generated by Django 5.0.7 on 2024-07-19 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artistas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artista',
            name='cpf',
            field=models.CharField(max_length=14, unique=True),
        ),
    ]
