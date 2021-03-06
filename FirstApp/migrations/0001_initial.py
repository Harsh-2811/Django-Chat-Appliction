# Generated by Django 3.1.4 on 2021-01-04 10:08

import datetime
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
            name='UserData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Dp', models.ImageField(upload_to='Chatapp')),
                ('active', models.BooleanField(default=False)),
                ('last_seen', models.DateTimeField(default=datetime.datetime(2021, 1, 4, 15, 38, 25, 939255))),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('decription', models.TextField(default='', max_length=200)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2021, 1, 4, 15, 38, 25, 939570))),
                ('room_members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.CharField(max_length=100)),
                ('timestamp', models.TimeField(auto_now_add=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_message', to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='FirstApp.room')),
            ],
        ),
    ]
