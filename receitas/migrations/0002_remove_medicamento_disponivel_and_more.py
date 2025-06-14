# Generated by Django 5.1.7 on 2025-04-29 05:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receitas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicamento',
            name='disponivel',
        ),
        migrations.AddField(
            model_name='medicamento',
            name='codigo_barras',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='medicamento',
            name='dosagem',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='medicamento',
            name='fabricante',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='medicamento',
            name='forma_farmaceutica',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='medicamento',
            name='preco',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='medicamento',
            name='nome',
            field=models.CharField(db_index=True, max_length=200, unique=True),
        ),
        migrations.CreateModel(
            name='Estoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(default=0)),
                ('medicamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='receitas.medicamento', unique=True)),
            ],
        ),
    ]
