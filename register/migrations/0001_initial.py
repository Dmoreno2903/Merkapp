# Generated by Django 4.2.7 on 2023-11-15 20:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Supermercado',
            fields=[
                ('nombre', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('latitud', models.CharField(max_length=50)),
                ('longitud', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('nombre', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Mercado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('producto', models.CharField(max_length=50)),
                ('costo', models.IntegerField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('supermercado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.supermercado')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.tipo')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
