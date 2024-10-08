# Generated by Django 5.1.1 on 2024-10-07 09:50

import django.db.models.deletion
import glyphs.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True)),
                ('tags', models.ManyToManyField(blank=True, to='glyphs.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Glyph',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(blank=True, max_length=100)),
                ('author_ip', models.GenericIPAddressField()),
                ('image', models.ImageField(upload_to=glyphs.models.upload_to)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('kage', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, to='glyphs.tag')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
