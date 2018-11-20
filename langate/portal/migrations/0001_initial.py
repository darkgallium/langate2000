# Generated by Django 2.1.3 on 2018-11-20 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import portal.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tournament', models.CharField(max_length=100)),
                ('team', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('role', models.CharField(choices=[(portal.models.Role('Player'), 'Player'), (portal.models.Role('Manager'), 'Manager'), (portal.models.Role('Guest'), 'Guest'), (portal.models.Role('Staff Member'), 'Staff Member'), (portal.models.Role('Administrator'), 'Administrator')], default='Player', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=15)),
                ('mac', models.CharField(max_length=17)),
                ('area', models.CharField(default='LAN', max_length=4)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(default='Computer', max_length=100)),
            ],
        ),
    ]
