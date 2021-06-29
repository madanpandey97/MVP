# Generated by Django 3.0 on 2021-06-28 10:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0005_auto_20210628_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='productview',
            name='last_viewed_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='productview',
            name='user',
        ),
        migrations.AddField(
            model_name='productview',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
