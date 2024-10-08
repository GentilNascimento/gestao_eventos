# Generated by Django 5.0.7 on 2024-07-19 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cpf', models.CharField(max_length=11, unique=True)),
                ('telefone', models.CharField(max_length=15, null=True)),
                ('banco', models.CharField(max_length=100)),
                ('tipo_chave_pix', models.CharField(choices=[('cel', 'Celular'), ('cnpj', 'CNPJ'), ('email', 'E-mail'), ('cpf', 'CPF')], default='cel', max_length=100)),
                ('chave_pix', models.CharField(max_length=100)),
            ],
        ),
    ]
