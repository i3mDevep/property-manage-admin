# Generated by Django 3.2.3 on 2021-08-26 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coproperties', '0002_property'),
    ]

    operations = [
        migrations.AddField(
            model_name='coproperty',
            name='logo_coproperty',
            field=models.ImageField(blank=True, null=True, upload_to='images/logo/coproperty', verbose_name='logo_coproperty'),
        ),
    ]
